import chromadb

from core.config import COLLECTION_NAME, VECTOR_DB_PATH


class ChromaVectorStore:
    def __init__(
        self,
        db_path: str = VECTOR_DB_PATH,
        collection_name: str = COLLECTION_NAME,
    ):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def count(self) -> int:
        return self.collection.count()

    def reset(self):
        # 새로 인덱싱할 때 기존 컬렉션을 깨끗하게 다시 만듭니다.
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_documents(self, documents: list[str], embeddings, ids: list[str]):
        self.collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            ids=ids,
        )

    def search(self, query_vector, k: int = 3):
        # 기존 Retriever/RAGPipeline이 기대하는 search 인터페이스를 맞춰 둡니다.
        result = self.query(query_embedding=query_vector, n_results=k)
        documents = result.get("documents", [[]])
        return documents[0] if documents else []

    def query(self, query_embedding, n_results: int = 3):
        return self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
        )
