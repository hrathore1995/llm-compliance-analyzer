from fastapi import APIRouter, UploadFile, File, Query
import shutil
from pathlib import Path

from app.ingestion.extractors import PDFExtractor, DocxExtractor
from app.rag.chunking import TextChunker
from app.rag.embeddings import EmbeddingsClient
from app.rag.vector_store import VectorStore
from app.rag.qa import ComplianceQA

# Router without prefix — prefix will be added in main.py
router = APIRouter(tags=["documents"])

# Folder for uploaded files
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF/DOCX, extract text, chunk it, embed it, and store in Qdrant."""
    file_path = UPLOAD_DIR / file.filename

    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    if file.filename.lower().endswith(".pdf"):
        extractor = PDFExtractor()
    elif file.filename.lower().endswith(".docx"):
        extractor = DocxExtractor()
    else:
        return {"error": "Unsupported file type"}

    text = extractor.extract(file_path)

    # Chunk text
    chunker = TextChunker()
    chunks = chunker.split(text)

    # Store chunks in Qdrant
    vector_store = VectorStore()
    metadatas = [{"filename": file.filename} for _ in chunks]
    vector_store.add(chunks, metadatas)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "status": "stored in Qdrant"
    }

@router.get("/search")
async def search_documents(
    query: str = Query(..., description="Search query text"),
    top_k: int = 3
):
    """Search stored documents in Qdrant and return raw chunks (no LLM)."""
    vector_store = VectorStore()
    results = vector_store.search(query, top_k=top_k)

    return [
        {
            "chunk": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in results
    ]

@router.get("/ask")
async def ask_documents(
    query: str = Query(..., description="Question to ask over stored documents"),
    top_k: int = 5
):
    """Ask a question over stored docs using RetrievalQA (LLM reasoning)."""
    qa = ComplianceQA()
    answer = qa.ask(query, top_k=top_k)
    return {"query": query, "answer": answer}
