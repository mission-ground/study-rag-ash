from rag.generation.generator import Generator
from rag.retrieval.retriever import Retriever


class RAGPipeline:
    def __init__(self, embedder, vector_store):
        self.retriever = Retriever(embedder, vector_store)
        self.generator = Generator()

    def ask(self, query, k: int = 3):
        # 검색으로 컨텍스트를 만든 뒤 생성 단계에 전달하는 가장 단순한 파이프라인입니다.
        documents = self.retriever.retrieve(query, k=k)
        context = "\n".join(documents)
        answer = self.generator.generate(query, context)
        return answer
