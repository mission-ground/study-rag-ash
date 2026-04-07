from fastapi import APIRouter
from pydantic import BaseModel, Field

from api.dependencies import get_rag_service
from core.config import PDF_PATH

router = APIRouter(prefix="/chat", tags=["chat"])


class IngestPreviewRequest(BaseModel):
    pdf_path: str = Field(default=PDF_PATH, description="PDF file path to inspect.")


class IngestRequest(BaseModel):
    pdf_path: str = Field(default=PDF_PATH, description="PDF file path to ingest.")
    reset: bool = Field(
        default=False,
        description="Reset the existing collection before ingesting the PDF again.",
    )


class SearchRequest(BaseModel):
    query: str = Field(..., description="Question to search for in the vector store.")
    n_results: int = Field(default=3, ge=1, le=20)


class AskRequest(BaseModel):
    query: str = Field(..., description="Question to answer using the RAG pipeline.")
    n_results: int = Field(default=3, ge=1, le=20)


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/preview")
def preview_ingest(request: IngestPreviewRequest):
    # 적재 전에 중간 산출물을 확인할 수 있는 읽기 전용 엔드포인트입니다.
    rag_service = get_rag_service()
    return rag_service.build_ingest_preview(file_path=request.pdf_path)


@router.post("/ingest")
def ingest_pdf(request: IngestRequest):
    rag_service = get_rag_service()
    return rag_service.ingest_pdf(file_path=request.pdf_path, reset=request.reset)


@router.post("/search")
def search_documents(request: SearchRequest):
    rag_service = get_rag_service()
    return rag_service.search(query=request.query, n_results=request.n_results)


@router.post("/ask")
def ask_question(request: AskRequest):
    # 기존 RAG 파이프라인 전체를 한 번에 실행하는 엔드포인트입니다.
    rag_service = get_rag_service()
    return rag_service.ask(query=request.query, n_results=request.n_results)
