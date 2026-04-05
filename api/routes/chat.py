from functools import lru_cache

from fastapi import APIRouter
from pydantic import BaseModel, Field

from core.config import PDF_PATH
from rag.retrieval.query_service import RAGQueryService

router = APIRouter(prefix="/chat", tags=["chat"])


class IngestRequest(BaseModel):
    pdf_path: str = Field(default=PDF_PATH, description="PDF file path to ingest.")
    reset: bool = Field(
        default=False,
        description="Reset the existing collection before ingesting the PDF again.",
    )


class SearchRequest(BaseModel):
    query: str = Field(..., description="Question to search for in the vector store.")
    n_results: int = Field(default=3, ge=1, le=20)


@lru_cache
def get_rag_service():
    return RAGQueryService()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/ingest")
def ingest_pdf(request: IngestRequest):
    rag_service = get_rag_service()
    return rag_service.ingest_pdf(file_path=request.pdf_path, reset=request.reset)


@router.post("/search")
def search_documents(request: SearchRequest):
    rag_service = get_rag_service()
    return rag_service.search(query=request.query, n_results=request.n_results)
