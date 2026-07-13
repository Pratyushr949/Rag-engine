<div align="center">

# 🚀 RAG Engine
### 💬 Chat with your PDFs using **Gemini AI + LangChain + ChromaDB + FastAPI + React**

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=600&size=24&duration=3500&pause=1000&color=00C2FF&center=true&vCenter=true&width=800&lines=Retrieval+Augmented+Generation+(RAG);Upload+PDF+%E2%9E%9C+Ask+Questions+%E2%9E%9C+Get+Answers;Powered+by+Gemini+AI+%F0%9F%A7%A0;FastAPI+%7C+React+%7C+LangChain+%7C+ChromaDB;Enterprise+Ready+Document+Assistant" />

---

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-red?style=for-the-badge)

</div>

---

# 🌟 Overview

**RAG Engine** is an end-to-end **Retrieval Augmented Generation (RAG)** application that allows users to upload PDF documents and interact with them using natural language.

Instead of relying only on Large Language Models, the application retrieves relevant document chunks from a Vector Database before generating responses, ensuring:

- ✅ Higher Accuracy
- ✅ Reduced Hallucination
- ✅ Context-aware Responses
- ✅ Enterprise-ready Architecture

---

# ✨ Features

## 📄 PDF Upload

- Upload any PDF document
- Automatic text extraction
- Secure file storage

---

## ✂ Intelligent Chunking

- Recursive text splitting
- Configurable chunk size
- Configurable overlap
- Optimized for semantic retrieval

---

## 🧠 AI Embeddings

- Gemini Embedding Model
- Semantic Vector Generation
- High Quality Embeddings

---

## 📦 Vector Database

- ChromaDB Integration
- Persistent Storage
- Fast Similarity Search

---

## 💬 Intelligent Chat

- Ask questions naturally
- Context-aware responses
- Retrieval before generation

---

## ⚡ Enterprise Ready

- Modular Architecture
- REST APIs
- Configurable Environment
- Logging Support
- Production Ready

---

# 🎯 Project Architecture

```text
                         ┌─────────────────────┐
                         │     React Frontend  │
                         └──────────┬──────────┘
                                    │
                           REST API Calls
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │      FastAPI Backend      │
                    └──────────┬────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Upload API        Chat API         Health API
              │
              ▼
      Document Loader
              │
              ▼
       Text Extraction
              │
              ▼
       Document Chunking
              │
              ▼
 Gemini Embedding Model
              │
              ▼
        ChromaDB Vector Store
              │
              ▼
      Similarity Search
              │
              ▼
    Relevant Context Retrieved
              │
              ▼
      Gemini LLM Generation
              │
              ▼
      Final Answer Returned
```

---

# ⚙ Workflow

```text
📄 Upload PDF

      │

      ▼

Extract Text

      │

      ▼

Split into Chunks

      │

      ▼

Generate Embeddings

      │

      ▼

Store in ChromaDB

      │

      ▼

User asks Question

      │

      ▼

Similarity Search

      │

      ▼

Relevant Context Retrieved

      │

      ▼

Gemini AI Generates Response

      │

      ▼

Answer Returned
```

---

# 🏗 Folder Structure

```
rag-engine/

│

├── backend/
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── uploads/
│   ├── vector_db/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── requirements.txt
```

---

# 🧩 Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | React.js |
| Styling | Tailwind CSS |
| Backend | FastAPI |
| Language | Python |
| LLM | Google Gemini |
| Embedding Model | Gemini Embedding |
| Vector Database | ChromaDB |
| Framework | LangChain |
| PDF Loader | PyPDF |
| API | REST |
| Environment | Python Virtual Environment |

---

# 🚀 Advantages

✅ Retrieval Augmented Generation

✅ Reduced Hallucinations

✅ Faster Semantic Search

✅ Enterprise Ready Architecture

✅ Modular Backend

✅ Configurable Environment

✅ Persistent Vector Storage

✅ Scalable Design

✅ Clean REST APIs

✅ Easy Deployment

---

# 📡 REST APIs

## Upload PDF

```
POST /api/upload
```

---

## Ask Question

```
POST /api/chat
```

---

## Health Check

```
GET /health
```

---

# 📚 RAG Pipeline

```
PDF

↓

Loader

↓

Chunking

↓

Embedding Model

↓

Vector Database

↓

Similarity Search

↓

Context Retrieval

↓

Gemini LLM

↓

Final Response
```

---

# 📈 Advantages over Traditional Chatbots

| Traditional Chatbot | RAG Engine |
|---------------------|-----------|
| Hallucinates | Uses Document Context |
| No Memory | Context Retrieval |
| Generic Answers | Document Specific |
| No Search | Semantic Search |
| Static Knowledge | Dynamic Knowledge |

---

# 🔮 Future Enhancements

- Multi PDF Support
- OCR Integration
- Image Extraction
- Hybrid Search (BM25 + Vector Search)
- Metadata Filtering
- Streaming Responses
- Authentication
- Docker Support
- Kubernetes Deployment
- Azure / AWS Deployment

---

# 📷 Screenshots

> Add screenshots here

```
assets/

home.png

upload.png

chat.png

result.png
```

---

# 💡 Installation

## Clone Repository

```bash
git clone https://github.com/Pratyushr949/Rag-engine.git
```

---

## Backend

```bash
cd backend

python -m venv venv

pip install -r requirements.txt

uvicorn app:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

```
GOOGLE_API_KEY=YOUR_API_KEY

MODEL_NAME=gemini-3.5-flash

CHUNK_SIZE=1000

CHUNK_OVERLAP=200

TOP_K=3
```

---

# ⭐ Why RAG?

✔ More Accurate

✔ Lower Hallucination

✔ Context Aware

✔ Enterprise Friendly

✔ Fast Retrieval

✔ Better User Experience

---

<div align="center">

# 🌟 If you found this project useful, don't forget to Star ⭐ the repository!

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=600&size=22&duration=3500&pause=1000&color=00FF99&center=true&vCenter=true&width=650&lines=Thank+You+for+Visiting!;Happy+Coding!+🚀;Built+with+❤️+using+FastAPI+%2B+React+%2B+Gemini"/>

</div>
