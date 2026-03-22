from core.config import DOCUMENT_TEXT_PATH
from rag.components.embedding.embedder import Embedder
from rag.components.vectorstore.faiss.vector_store import VectorStore
from rag.ingestion.chunker import Chunker


class IndexBuilder:
    def __init__(self):
        self.embedder = Embedder()
        self.chunker = Chunker()
        self.vector_store = VectorStore()

    def build(self):
        documents = self.load_documents()
        chunks = self.chunk_documents(documents)
        vectors = self.embed_chunks(chunks)
        self.vector_store.add_documents(vectors, chunks)
        return self.embedder, self.vector_store

    def load_documents(self):
        docs = []

        with open(DOCUMENT_TEXT_PATH, "r", encoding="utf-8") as f:
            for line in f:
                docs.append(line.strip())

        return docs

    def chunk_documents(self, documents):
        chunks = []
        for doc in documents:
            doc_chunks = self.chunker.split(doc)
            chunks.extend(doc_chunks)
        return chunks
