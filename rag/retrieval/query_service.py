from rag.components.embedding.sentence_transformer_embedder import (
    SentenceTransformerEmbedder,
)
from rag.components.vectorstore.chroma.chroma_store import ChromaVectorStore
from rag.ingestion.pdf_extractor import extract_korean_english_text


class RAGQueryService:
    def __init__(self):
        self.embedder = SentenceTransformerEmbedder()
        self.vectorstore = ChromaVectorStore()

    def extract_documents(self, file_path: str):
        pdf_text = extract_korean_english_text(file_path)
        documents = [doc.strip() for doc in pdf_text.split("\n") if doc.strip()]
        return pdf_text, documents

    def preview_ingest(self, file_path: str):
        pdf_text, documents = self.extract_documents(file_path)
        embeddings = self.embedder.embed_documents(documents) if documents else []

        embedding_dimension = 0
        sample_embedding = []
        if len(documents) > 0:
            embedding_dimension = int(len(embeddings[0]))
            sample_embedding = embeddings[0][:8].tolist()

        return {
            "file_path": file_path,
            "raw_text": pdf_text,
            "documents": documents,
            "document_count": len(documents),
            "embedding_dimension": embedding_dimension,
            "sample_embedding": sample_embedding,
            "vector_store_count": self.vectorstore.count(),
        }

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

        _, documents = self.extract_documents(file_path)
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
        distances = raw_result.get("distances", [[]])
        ids = raw_result.get("ids", [[]])

        items = []
        document_list = documents[0] if documents else []
        distance_list = distances[0] if distances else []
        id_list = ids[0] if ids else []

        for index, document in enumerate(document_list):
            items.append(
                {
                    "rank": index + 1,
                    "id": id_list[index] if index < len(id_list) else None,
                    "distance": distance_list[index] if index < len(distance_list) else None,
                    "document": document,
                }
            )

        return {
            "query": query,
            "query_embedding_dimension": int(len(query_embedding)),
            "query_embedding_preview": query_embedding[:8].tolist(),
            "documents": document_list,
            "items": items,
            "raw": raw_result,
        }
