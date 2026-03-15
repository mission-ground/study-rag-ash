import faiss
import numpy as np

# 벡터 저장과 검색을 처리하는 클래스
class VectorStore:

    def __init__(self, dimension=384):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    # 1. 벡터 저장
    def add_documents(self, vectors, docs):
        self.index.add(np.array(vectors))
        self.documents.extend(docs)

    # 2. 벡터 검색
    def search(self, query_vector, k=3):

        distances, indices = self.index.search(query_vector, k)

        results = []

        for idx in indices[0]:
            results.append(self.documents[idx])

        return results