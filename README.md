# 🚀 Hybrid RAG Engine with Open Knowledge Format (OKF)

Enterprise-grade Retrieval-Augmented Generation using FastAPI, React,
Gemini, LangChain and ChromaDB.

## Badges

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge)

## Overview

Hybrid RAG Engine combines semantic retrieval with Open Knowledge Format
(OKF) for explainable, knowledge-aware document question answering.

## Architecture

``` text
React
  |
FastAPI
  |
Upload -> Loader -> Chunking -> Embeddings -> ChromaDB
                          |
                          +-> Entity Extraction -> Relationship Extraction -> OKF
                                   |
                              Hybrid Retrieval
                                   |
                                Gemini
```

## Features

-   PDF Upload
-   Multi-document RAG
-   ChromaDB
-   Gemini
-   OKF
-   Knowledge Graph
-   Hybrid Retrieval
-   REST APIs

## Tech Stack

  Layer       Technology
  ----------- --------------
  Frontend    React + Vite
  Backend     FastAPI
  AI          Gemini
  Framework   LangChain
  Vector DB   ChromaDB
  Knowledge   OKF JSON

## Installation

``` bash
git clone https://github.com/Pratyushr949/Rag-engine.git
python -m venv venv
pip install -r requirements.txt
```

## Environment

``` env
GOOGLE_API_KEY=YOUR_API_KEY
MODEL_NAME=gemini-1.5-flash
```

## Run

``` bash
cd backend
uvicorn app:app --reload
```

``` bash
cd frontend
npm install
npm run dev
```

## APIs

-   POST /api/upload
-   POST /api/chat
-   GET /api/knowledge
-   GET /api/entities
-   GET /api/relationships
-   GET /api/graph
-   DELETE /api/reset

## Roadmap

-   Docker
-   Neo4j
-   Redis
-   Kubernetes
-   CI/CD

## License

MIT
