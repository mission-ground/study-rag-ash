from functools import lru_cache

from app.services.rag_app_service import RAGAppService


@lru_cache
def get_rag_service():
    # 요청마다 모델과 벡터스토어 클라이언트를 다시 만들지 않도록 캐시합니다.
    return RAGAppService()
