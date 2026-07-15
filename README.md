::: {align="center"}
# 🚀 Hybrid RAG Engine

### **Knowledge-Enhanced Retrieval using Open Knowledge Format (OKF)**

`<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=700&size=24&duration=3500&pause=900&color=00C2FF&center=true&vCenter=true&width=900&lines=Hybrid+Retrieval+Augmented+Generation;FastAPI+%7C+React+%7C+Gemini+%7C+LangChain;Open+Knowledge+Format+(OKF);Knowledge+Graph+Powered+AI;Enterprise+Ready+Document+Assistant" />`{=html}

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react)
![LangChain](https://img.shields.io/badge/LangChain-RAG-success?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange?style=for-the-badge&logo=google)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
:::

------------------------------------------------------------------------

# 📖 Overview

Hybrid RAG Engine is an enterprise-style Retrieval Augmented Generation
system that combines **semantic vector retrieval** with **Open Knowledge
Format (OKF)** and a **Knowledge Graph**.

Instead of relying only on vector similarity, the system extracts
entities and relationships from uploaded PDFs, generates structured
knowledge, and performs **Hybrid Retrieval** before sending context to
Gemini.

------------------------------------------------------------------------

# ✨ Key Features

-   📄 Multi-PDF Upload
-   🧩 Intelligent Chunking
-   🧠 Gemini Embeddings
-   📦 ChromaDB Vector Storage
-   🕸 Entity Extraction
-   🔗 Relationship Extraction
-   📚 Open Knowledge Format (OKF)
-   🌐 Knowledge Graph Visualization
-   🔥 Hybrid Retrieval
-   💬 Conversational Chat
-   📊 Explainable Responses
-   ⚡ REST APIs
-   🎨 React Dashboard
-   📈 Production-Ready Modular Architecture

------------------------------------------------------------------------

# 🏗 System Architecture

``` text
                    ┌─────────────────────────────┐
                    │       React Frontend        │
                    └──────────────┬──────────────┘
                                   │
                            REST API Calls
                                   │
                    ┌──────────────▼──────────────┐
                    │      FastAPI Backend        │
                    └──────────────┬──────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
      Upload API               Chat API              Knowledge API
          │
          ▼
      PDF Loader
          │
          ▼
   Text Extraction
          │
   ┌──────┴───────────────┐
   ▼                      ▼
RAG Pipeline         OKF Pipeline
   │                      │
Chunking          Entity Extraction
   │                      │
Embeddings     Relationship Extraction
   │                      │
ChromaDB         OKF JSON Generator
   └──────────────┬───────────────┘
                  ▼
          Hybrid Fusion Retriever
                  ▼
             Gemini LLM
                  ▼
          Explainable Answer
```

------------------------------------------------------------------------

# 🔄 End-to-End Workflow

``` text
User Uploads PDF
        │
        ▼
Extract Document Text
        │
        ▼
Split into Chunks
        │
        ├──────────────┐
        ▼              ▼
Generate        Extract Entities
Embeddings      Extract Relations
        │              │
        ▼              ▼
 ChromaDB         OKF Generator
        └──────┬───────┘
               ▼
      Hybrid Context Builder
               ▼
        User asks Question
               ▼
   Vector Search + OKF Search
               ▼
          Context Fusion
               ▼
         Gemini Generation
               ▼
      Final Explainable Answer
```

------------------------------------------------------------------------

# 🧠 Pipelines

## RAG Pipeline

PDF → Chunking → Embeddings → ChromaDB → Similarity Search → Gemini

## OKF Pipeline

PDF → Entity Extraction → Relationship Extraction → OKF JSON → Knowledge
Store

## Hybrid Retrieval Pipeline

Vector Retrieval + OKF Retrieval → Context Fusion → Gemini → Answer

------------------------------------------------------------------------

# 📂 Folder Structure

``` text
rag-engine/
├── backend/
│   ├── app.py
│   ├── config/
│   ├── routes/
│   ├── services/
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   ├── fusion_retriever.py
│   │   ├── entity_extractor.py
│   │   ├── relationship_extractor.py
│   │   ├── okf_generator.py
│   │   └── knowledge_storage.py
│   ├── uploads/
│   ├── vector_db/
│   └── knowledge_store/
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# 🛠 Technology Stack

  Category          Technology
  ----------------- -----------------------------
  Frontend          React, Vite, Tailwind CSS
  Backend           FastAPI, Uvicorn
  LLM               Google Gemini
  Framework         LangChain
  Vector DB         ChromaDB
  Knowledge Layer   Open Knowledge Format (OKF)
  Graph Engine      NetworkX
  Language          Python
  API               REST

------------------------------------------------------------------------

# 🚀 Installation

``` bash
git clone https://github.com/Pratyushr949/Rag-engine.git
cd Rag-engine

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

cd frontend
npm install
```

------------------------------------------------------------------------

# 🔑 Environment Variables

``` env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
MODEL_NAME=gemini-1.5-flash
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=4
```

------------------------------------------------------------------------

# ▶ Running

Backend

``` bash
cd backend
uvicorn app:app --reload
```

Frontend

``` bash
cd frontend
npm run dev
```

------------------------------------------------------------------------

# 🌍 REST APIs

  Method   Endpoint             Purpose
  -------- -------------------- -------------------------
  POST     /api/upload          Upload PDFs
  POST     /api/chat            Ask questions
  GET      /api/knowledge       OKF data
  GET      /api/entities        Extracted entities
  GET      /api/relationships   Extracted relationships
  GET      /api/graph           Graph data
  DELETE   /api/reset           Reset session

------------------------------------------------------------------------

# 📈 Advantages

-   Lower hallucinations
-   Explainable AI
-   Semantic + Structured retrieval
-   Knowledge graph support
-   Modular architecture
-   Easy extensibility
-   Production-ready APIs

------------------------------------------------------------------------

# 🗺 Roadmap

-   Docker
-   Redis Cache
-   Neo4j Integration
-   Authentication
-   Multi-user support
-   Cloud Deployment
-   Kubernetes
-   CI/CD

------------------------------------------------------------------------

# 📷 Screenshots

Replace with your screenshots:

-   Home
-   Upload
-   Chat
-   Knowledge
-   Graph
-   Swagger

------------------------------------------------------------------------

# 🤝 Contributing

Fork → Create Branch → Commit → Push → Pull Request

------------------------------------------------------------------------

# 📄 License

MIT License

------------------------------------------------------------------------

::: {align="center"}
## ⭐ Star this repository if you found it useful!

**Built with ❤️ using FastAPI, React, Gemini, LangChain, ChromaDB and
Open Knowledge Format (OKF).**
:::
