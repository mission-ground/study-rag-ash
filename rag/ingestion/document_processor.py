from rag.ingestion.chunker import Chunker
from rag.ingestion.pdf_extractor import extract_korean_english_text


class DocumentProcessor:
    def __init__(self):
        self.chunker = Chunker()

    def extract_text(self, file_path: str) -> str:
        return extract_korean_english_text(file_path)

    def split_documents(self, text: str) -> list[str]:
        return [line.strip() for line in text.splitlines() if line.strip()]

    def chunk_documents(self, documents: list[str]) -> list[str]:
        chunks = []
        for document in documents:
            chunks.extend(self.chunker.split(document))
        return [chunk.strip() for chunk in chunks if chunk.strip()]
