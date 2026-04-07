import numpy as np


class Retriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = 3):
        # 사용자 질문을 벡터로 바꾼 뒤 유사도 검색에 사용합니다.
        query_vector = self.embedder.embed(query)
        query_vector = np.array([query_vector])
        documents = self.vector_store.search(query_vector, k=k)
        return documents
