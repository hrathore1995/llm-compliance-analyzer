# LLM Compliance Analyzer

[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1A1A1A?logo=chainlink\&logoColor=white)](https://www.langchain.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

The **LLM Compliance Analyzer** is a system designed to analyze compliance documents such as privacy policies, healthcare regulations, or internal corporate guidelines. It allows users to:

* Upload documents (PDF/DOCX).
* Search for relevant content within stored chunks.
* Ask questions and receive LLM-powered answers that combine retrieval and reasoning.
* Check compliance rules against uploaded documents.

This system leverages **Retrieval-Augmented Generation (RAG)** to enhance large language model (LLM) responses with context directly retrieved from documents.

---

## Use Case

Organizations in regulated industries (finance, healthcare, legal, corporate governance) face compliance risks when employees must work with large, complex policy documents.

This project provides:

* Faster **compliance checks** on uploaded policies.
* Instant **answers to regulatory questions** with citations from documents.
* Ability to **search raw text chunks** without waiting for an LLM.

In practice, a compliance officer, auditor, or data protection analyst could use this tool to confirm whether documents mention key requirements (e.g., GDPR, HIPAA, or PCI DSS).

---

## How It Works (RAG Pipeline)

1. **Document Upload**

   * PDF or DOCX uploaded via the frontend.
   * Text is extracted using **PyPDF2** or **python-docx**.

2. **Chunking**

   * Extracted text is split into semantic chunks for efficient retrieval.

3. **Embedding & Storage**

   * Chunks are embedded using **OpenAI embeddings** via `langchain-openai`.
   * Stored in **Qdrant** (vector database).

4. **Retrieval-Augmented Generation (RAG)**

   * For user queries, top-K relevant chunks are retrieved.
   * Chunks are passed to the LLM, which generates a context-aware response.

5. **Rule Checking**

   * Compliance rules (JSON-based) can be run in parallel for simple keyword/pattern checks.
   * LLM reasoning + rules provide hybrid verification.

---

## Tech Stack

* **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
* **LLM Orchestration**: [LangChain](https://www.langchain.com/)
* **Vector Database**: [Qdrant](https://qdrant.tech/)
* **Frontend**: Simple HTML, CSS, and JS served via **Nginx**
* **Containerization**: [Docker](https://www.docker.com/) with Docker Compose
* **Embeddings**: [OpenAI](https://platform.openai.com/)

---

## Project Structure

```
llm_compliance_analyzer/
│
├── app/
│   ├── api/                # FastAPI endpoints (upload, search, ask)
│   │   └── main.py
│   │   └── documents.py
│   ├── compliance/         # Rule-based compliance checking
│   │   └── rules.py
│   ├── ingestion/          # Document extractors (PDF, DOCX)
│   ├── rag/                # RAG pipeline (chunking, embeddings, vector store, QA)
│   │   └── chunking.py
│   │   └── embeddings.py
│   │   └── vector_store.py
│   │   └── qa.py
│
├── frontend/               # Nginx-served static frontend
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── nginx.conf
│
├── data/uploads/           # Uploaded docs (ignored in git)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .gitignore
├── .dockerignore
└── README.md
```

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/llm_compliance_analyzer.git
cd llm_compliance_analyzer
```

### 2. Configure Environment

Create a `.env` file with your OpenAI key:

```env
OPENAI_API_KEY=sk-...
```

### 3. Start with Docker Compose

```bash
docker compose up --build
```

### 4. Access the App

* **Frontend**: [http://localhost](http://localhost)
* **Backend**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Qdrant**: [http://localhost:6333](http://localhost:6333)

---

## Future Improvements

* Add user authentication and role-based access.
* Store citations with each LLM answer.
* Expand compliance rules (e.g., regex-based detection).
* Enhance frontend with React + shadcn/ui.
* Support additional document formats (HTML, TXT).

---

This project demonstrates how **Docker + FastAPI + LangChain + Qdrant** can be combined to create an end-to-end compliance analyzer with both **LLM reasoning** and **rule-based validation**.
