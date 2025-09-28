from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

import app.api.documents as documents

app = FastAPI(title="LLM Compliance Analyzer", version="0.1.0")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running 🚀"}

# Mount all document-related routes under /api/documents
app.include_router(documents.router, prefix="/api/documents")
