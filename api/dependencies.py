from functools import lru_cache

from rag.retrieval.query_service import RAGQueryService


@lru_cache
def get_rag_service():
    return RAGQueryService()
