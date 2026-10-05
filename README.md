# DocQuery

DocQuery is a full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content through a conversational interface.

The application processes uploaded documents, creates semantic embeddings, retrieves relevant document sections using FAISS, and generates context-aware responses using a locally hosted Phi-3 Mini model through Ollama.

## Features

- Upload and process PDF documents
- Automatic document chunking
- Semantic vector search using FAISS
- Hugging Face sentence-transformer embeddings
- Context-aware question answering
- Local LLM inference using Ollama
- React-based chat interface
- FastAPI backend
- Source-aware document retrieval
- No external LLM API required

## Architecture

```text
                    ┌─────────────────────┐
                    │     React Frontend  │
                    │                     │
                    │  PDF Upload + Chat  │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    │                     │
                    │  Document Processing│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Text Chunking     │
                    │                     │
                    │ LangChain Splitter  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │     Embeddings      │
                    │                     │
                    │ SentenceTransformers│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │       FAISS         │
                    │                     │
                    │ Semantic Retrieval  │
                    └──────────┬──────────┘
                               │
                         Relevant Context
                               │
                    ┌──────────▼──────────┐
                    │     Ollama          │
                    │                     │
                    │    Phi-3 Mini       │
                    └──────────┬──────────┘
                               │
                               ▼
                         Generated Answer


## RAG Pipeline

DocQuery follows a Retrieval-Augmented Generation (RAG) pipeline:

1. The user uploads a PDF document.
2. The FastAPI backend receives the document.
3. PDF content is extracted using `PyPDFLoader`.
4. The extracted content is split into smaller chunks.
5. Each chunk is converted into a vector embedding using a Sentence Transformer model.
6. The embeddings are stored in a FAISS vector index.
7. When the user submits a question, FAISS performs semantic similarity search.
8. The most relevant document chunks are retrieved.
9. The retrieved context is passed to Phi-3 Mini through Ollama.
10. The generated response is returned to the React frontend.

This allows the LLM to answer questions based on the uploaded document rather than relying only on its pretrained knowledge.

---

## Tech Stack

### Frontend

- React
- Vite
- Styled Components
- Axios
- React Dropzone

### Backend

- Python
- FastAPI
- LangChain
- PyPDF
- FAISS
- Sentence Transformers

### AI / LLM

- Ollama
- Microsoft Phi-3 Mini
- Hugging Face Sentence Transformers

---

## Project Structure

```text
DocQuery/
│
├── backend_chatdoc.py
│
├── front-chatdoc/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   └── FileUpload.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── eslint.config.js
│
├── .gitignore
└── README.md


Copy everything below directly into your README.md:
# DocQuery

DocQuery is a full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and interact with them through a conversational interface.

---

## Project Structure

```text
DocQuery/
│
├── backend_chatdoc.py
│
├── front-chatdoc/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   └── FileUpload.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── eslint.config.js
│
├── .gitignore
└── README.md

The following directories are generated locally and are intentionally excluded from Git:
venv/
node_modules/
faiss_vector_store/
uploaded_documents/

## How It Works
1. Document Upload
The React frontend allows the user to upload a PDF document.
The file is sent to the FastAPI backend through:
POST /upload/

The backend saves and processes the document.
2. Document Processing
The PDF is loaded using PyPDFLoader.
The extracted text is divided into smaller chunks using LangChain text splitters.
Each chunk retains document metadata such as:
- Source document
- Page number
3. Embedding Generation
Each document chunk is converted into a numerical vector representation using:
sentence-transformers/all-mpnet-base-v2

These embeddings represent the semantic meaning of the document content.
4. Vector Storage
The generated embeddings are stored in a FAISS vector index.
FAISS enables efficient similarity search over the document embeddings.
5. Question Answering
When the user asks a question, the backend performs a similarity search:
User Question
      ↓
Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Document Chunks

The retrieved chunks are then provided as context to the LLM.
6. Local LLM Generation
DocQuery uses Phi-3 Mini through Ollama:
Retrieved Context
       +
User Question
       ↓
   Phi-3 Mini
       ↓
Generated Answer

The model is instructed to answer using the retrieved document context.
API Endpoints
Upload Document
POST /upload/

Uploads and processes a PDF document.
Query Document
POST /query/

Accepts a question and retrieves relevant document context before generating an answer.
Example request:
{
  "question": "What technologies are mentioned in the document?"
}

API Documentation
FastAPI automatically provides interactive API documentation at:
http://localhost:8000/docs

Installation
Prerequisites
Make sure the following are installed:
- Python 3.10+
- Node.js
- npm
- Ollama
Backend Setup
Clone the repository:
git clone https://github.com/YOUR_USERNAME/DocQuery.git
cd DocQuery

Create a Python virtual environment:
python3 -m venv venv

Activate the environment:
source venv/bin/activate

Install the required Python packages:
pip install --upgrade pip

pip install fastapi uvicorn python-dotenv langchain \
langchain-community langchain-huggingface \
langchain-text-splitters faiss-cpu \
sentence-transformers pypdf python-multipart requests

Ollama Setup
Install Ollama from the official website:
https://ollama.com/
Pull the Phi-3 Mini model:
ollama pull phi3:mini

Start the Ollama server:
ollama serve

You can verify the model using:
ollama run phi3:mini

No external LLM API key is required.
Start the Backend
From the project root:
python backend_chatdoc.py

The backend will start at:
http://localhost:8000

You can access the FastAPI Swagger documentation at:
http://localhost:8000/docs

Start the Frontend
Open another terminal:
cd front-chatdoc

Install dependencies:
npm install

Start the development server:
npm run dev

The frontend will normally be available at:
http://localhost:5173

Example Usage
1. Start the Ollama server.
2. Start the FastAPI backend.
3. Start the React frontend.
4. Open the application in your browser.
5. Upload a PDF document.
6. Wait for document processing to complete.
7. Ask a question about the uploaded document.
8. The application retrieves relevant document chunks and generates an answer using Phi-3 Mini.
Example Questions
Summarise this document.

What technologies are mentioned in the document?

What are the main requirements?

Explain the responsibilities described in the document.

What are the key points from page 2?

## Local-First AI
One of the main design choices in DocQuery is local LLM inference.
Instead of sending prompts to an external LLM API, the application uses Ollama to run Phi-3 Mini locally.
Benefits
- No external LLM API key
- No per-request API cost
- Documents remain available for local processing
- Easy local development
- Greater control over the inference environment

## Key Implementation Details
### Semantic Search
FAISS is used to perform vector similarity search over document embeddings.
This allows the application to retrieve content based on semantic meaning rather than simple keyword matching.
### Context-Aware Generation
The retrieved document chunks are included in the prompt sent to Phi-3 Mini.
The model is instructed to answer using the retrieved context and avoid relying on unrelated external information.
### Upload State Management
The frontend prevents users from querying the backend before document processing has completed.
The workflow is:
PDF Selected
     ↓
Upload Started
     ↓
Backend Processes PDF
     ↓
FAISS Index Updated
     ↓
Upload Completed
     ↓
Chat Enabled

This prevents a query from being sent while the document is still being processed.
## Future Improvements
The current version provides the core RAG workflow. Possible future improvements include:
- Multi-document collections
- Improved source and page citations in the UI
- Streaming LLM responses
- Conversation history
- Hybrid keyword + semantic search
- Retrieval reranking
- Background document processing
- Kafka-based asynchronous ingestion
- Docker deployment
- Authentication
- User-specific document collections
- Cloud deployment
- Better document parsing for tables and complex layouts