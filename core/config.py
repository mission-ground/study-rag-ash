# config.py
# .env 파일에서 설정값을 읽습니다.

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PDF_PATH = next(BASE_DIR.glob("*.pdf"), BASE_DIR / "document.pdf")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_PATH = os.getenv("PDF_PATH", str(DEFAULT_PDF_PATH))
DOCUMENT_TEXT_PATH = os.getenv("DOCUMENT_TEXT_PATH", str(BASE_DIR / "docs" / "a.text"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K = int(os.getenv("TOP_K", 3))
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(BASE_DIR / "my_vector_db"))

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "money_psychology_docs"
