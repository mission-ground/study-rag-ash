from rag.components.embedding.sentence_transformer_embedder import (
    SentenceTransformerEmbedder,
)
from rag.components.vectorstore.chroma.chroma_store import ChromaVectorStore
from rag.ingestion.document_processor import DocumentProcessor
from rag.rag_pipeline import RAGPipeline


class RAGAppService:
    def __init__(self):
        # 기존 RAG 구성 요소를 유지한 채 앱에서 바로 쓸 수 있게 묶습니다.
        self.processor = DocumentProcessor()
        self.embedder = SentenceTransformerEmbedder()
        self.vectorstore = ChromaVectorStore()
        self.pipeline = RAGPipeline(self.embedder, self.vectorstore)

    def build_ingest_preview(self, file_path: str):
        # 벡터 DB를 바꾸지 않고 각 적재 단계를 미리 확인합니다.
        raw_text = self.processor.extract_text(file_path)
        documents = self.processor.split_documents(raw_text)
        chunks = self.processor.chunk_documents(documents)
        embeddings = self.embedder.embed_documents(chunks) if chunks else []

        embedding_dimension = 0
        sample_embedding = []
        if chunks:
            embedding_dimension = int(len(embeddings[0]))
            sample_embedding = embeddings[0][:8].tolist()

        return {
            "file_path": file_path,
            "raw_text": raw_text,
            "documents": documents,
            "chunks": chunks,
            "document_count": len(documents),
            "chunk_count": len(chunks),
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
                "message": "Vector store already contains indexed chunks.",
                "item_count": self.vectorstore.count(),
                "file_path": file_path,
            }

        preview = self.build_ingest_preview(file_path)
        chunks = preview["chunks"]
        embeddings = self.embedder.embed_documents(chunks) if chunks else []
        ids = [f"chunk_{i}" for i in range(len(chunks))]

        # 미리보기 파이프라인이 끝난 뒤에만 실제 벡터 저장을 수행합니다.
        if chunks:
            self.vectorstore.add_documents(
                documents=chunks,
                embeddings=embeddings,
                ids=ids,
            )

        return {
            "status": "ingested",
            "message": "PDF content was indexed successfully.",
            "item_count": self.vectorstore.count(),
            "document_count": preview["document_count"],
            "chunk_count": preview["chunk_count"],
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
            "items": items,
            "raw": raw_result,
        }

    def ask(self, query: str, n_results: int = 3):
        # 예전 파이프라인을 그대로 재사용해 검색과 생성을 연결합니다.
        answer = self.pipeline.ask(query, k=n_results)
        return {"query": query, "answer": answer}
