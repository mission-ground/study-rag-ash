from backend.service.rag.components.embedding.embedder import Embedder
from backend.service.rag.ingestion.chunker import Chunker
from backend.service.rag.components.vectorstore.faiss.vector_store import VectorStore

#ingestion = 데이터를 시스템에 넣는 과정
class IndexBuilder:

    def __init__(self):
        
        self.embedder = Embedder()          # 1. 처리할 문서를 임베딩 처리하기 위해 모델을 로딩한다.
        self.chunker = Chunker()            # 2. load 된 데이터를 청킹할 청커를 준비한다.
        self.vector_store = VectorStore()   # 3. 처리된 문서 데이터를 저장할 벡터DB 준비한다.

    # 실제로 처리되는 곳
    def build(self):

        documents = self.load_documents()
        chunks = self.chunk_documents(documents)
        vectors = self.embed_chunks(chunks)
        self.vector_store.add_documents(vectors, chunks)
        return self.embedder, self.vector_store
    
    # 추후 Loader를 따로 파일 만들어야 겠다.
    def load_documents(self):

        docs = []

        
        with open("data/documents.txt", "r", encoding="utf-8") as f:

            for line in f:
                docs.append(line.strip())

        return docs
    
    def chunk_documents(self, documents):

        chunks = []
        for doc in documents:

            doc_chunks = self.chunker.split(doc)
            chunks.extend(doc_chunks)
        return chunks
    

    