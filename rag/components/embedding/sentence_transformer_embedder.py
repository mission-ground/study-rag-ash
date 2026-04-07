from sentence_transformers import SentenceTransformer

from core.config import EMBEDDING_MODEL_NAME


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        return self.model.encode(text)

    def embed_documents(self, documents: list[str]):
        return self.model.encode(documents)

    def embed_query(self, query: str):
        return self.model.encode(query)
