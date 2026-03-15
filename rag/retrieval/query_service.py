from backend.service.rag.ingestion.pdf_extractor import extract_korean_english_text
from backend.service.rag.components.embedding.sentence_transformer_embedder import (
    SentenceTransformerEmbedder,
)
from backend.service.rag.components.vectorstore.chroma.chroma_store import (
    ChromaVectorStore,
)


class RAGQueryService:
    def __init__(self):
        self.embedder = SentenceTransformerEmbedder()
        self.vectorstore = ChromaVectorStore()

    def ingest_pdf(self, file_path: str):
        pdf_text = extract_korean_english_text(file_path)
        documents = pdf_text.split("\n")

        embeddings = self.embedder.embed_documents(documents)
        ids = [f"doc_{i}" for i in range(len(documents))]

        if self.vectorstore.count() == 0:
            self.vectorstore.add_documents(
                documents=documents,
                embeddings=embeddings,
                ids=ids,
            )
            print(f"총 {self.vectorstore.count()}개의 데이터가 벡터 DB에 성공적으로 저장되었습니다!")
        else:
            print(f"이미 {self.vectorstore.count()}개의 데이터가 벡터 DB에 성공적으로 저장되어 있습니다!")

    def search(self, query: str, n_results: int = 3):
        query_embedding = self.embedder.embed_query(query)
        return self.vectorstore.query(query_embedding=query_embedding, n_results=n_results)