from rag.components.embedding.sentence_transformer_embedder import (
    SentenceTransformerEmbedder,
)
from rag.components.vectorstore.chroma.chroma_store import ChromaVectorStore
from rag.ingestion.pdf_extractor import extract_korean_english_text


class RAGQueryService:
    def __init__(self):
        self.embedder = SentenceTransformerEmbedder()
        self.vectorstore = ChromaVectorStore()

    def ingest_pdf(self, file_path: str, reset: bool = False):
        if reset:
            self.vectorstore.reset()

        if self.vectorstore.count() > 0:
            return {
                "status": "skipped",
                "message": "Vector store already contains indexed documents.",
                "document_count": self.vectorstore.count(),
                "file_path": file_path,
            }

        pdf_text = extract_korean_english_text(file_path)
        documents = [doc for doc in pdf_text.split("\n") if doc.strip()]
        embeddings = self.embedder.embed_documents(documents)
        ids = [f"doc_{i}" for i in range(len(documents))]

        self.vectorstore.add_documents(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
        )

        return {
            "status": "ingested",
            "message": "PDF content was indexed successfully.",
            "document_count": self.vectorstore.count(),
            "file_path": file_path,
        }

    def search(self, query: str, n_results: int = 3):
        query_embedding = self.embedder.embed_query(query)
        raw_result = self.vectorstore.query(
            query_embedding=query_embedding,
            n_results=n_results,
        )
        documents = raw_result.get("documents", [[]])

        return {
            "query": query,
            "documents": documents[0] if documents else [],
            "raw": raw_result,
        }
