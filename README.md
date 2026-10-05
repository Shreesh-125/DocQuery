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
