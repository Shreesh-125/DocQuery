from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import os
import requests
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import shutil  # For saving uploaded files
from pathlib import Path  # For safer path handling
from typing import List  # Import List for type hinting
from langchain_community.document_loaders import PyPDFLoader
from fastapi.middleware.cors import CORSMiddleware


#FastAPI
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Constants
VECTOR_STORE_PATH = "faiss_vector_store"
UPLOAD_FOLDER = "uploaded_documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = None
def load_vector_store():
    global vector_store
    try:
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        print("Vector store loaded successfully from disk.")
    except Exception as e:
        print(f"Error loading vector store from disk: {e}. Creating a new one.")
        vector_store = FAISS.from_texts(["Initial empty document."], embedding=embeddings)
        vector_store.save_local(VECTOR_STORE_PATH)

load_vector_store()  # Load on application startup

class QueryRequest(BaseModel):
    question: str

def query(question: str):
    global vector_store
    if vector_store is None:
        return {"answer": "Vector store is not initialized. Please upload a document."}

    relevant_docs = vector_store.similarity_search(question, k=2)
    print(f"len(relevant_docs): {len(relevant_docs)}")
    print(f"relevant_docs: {relevant_docs}")
    context = "\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
    You are an AI assistant.

    Answer the question using ONLY the provided context.
    Do not use outside information.
    If the answer cannot be found in the context, say:
    "I need more context."

    Context:
    {context}

    Question:
    {question}
    """

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "phi3:mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Ollama error: {response.text}"
        )

    result = response.json()

    return {
        "answer": result["message"]["content"],
        "sources": [
            {
                "document": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "Unknown")
            }
            for doc in relevant_docs
        ],
    }


def process_document(file_path: str):
    """Loads and splits a PDF while preserving source metadata."""
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )

        texts = text_splitter.split_documents(documents)

        for text in texts:
            text.metadata["source"] = os.path.basename(file_path)
            text.metadata["page"] = text.metadata.get("page", 0) + 1

        return texts

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF document: {e}"
        )

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    global vector_store  # Access the global variable

    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        documents = process_document(file_path)

        new_vector_store = FAISS.from_documents(
            documents,
            embedding=embeddings
        )
        if vector_store is None:
            vector_store = new_vector_store
        else:
            vector_store.merge_from(new_vector_store) # Fixed merging
        vector_store.save_local(VECTOR_STORE_PATH) # Save updated store
        
        if hasattr(vector_store, 'index') and hasattr(vector_store.index, 'ntotal'):
            index_size = vector_store.index.ntotal
            print(f"FAISS index Size: {index_size}")
        else:
            print("Could not determine FAISS index size.")

        return {"filename": file.filename, "message": "PDF document uploaded and processed successfully."}

    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) # Return error as HTTPException
    finally:
        file.file.close()  # Ensure file is closed



@app.post("/query/")
async def ask_question(request: QueryRequest):
    return query(request.question)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
