# config.py
# .env 파일에서 설정값을 읽어온다
# pip install python-dotenv

from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일을 읽어서 환경변수로 등록

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_PATH       = os.getenv("PDF_PATH", "document.pdf")
CHUNK_SIZE     = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP  = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K          = int(os.getenv("TOP_K", 3))
EMBED_MODEL    = os.getenv("EMBED_MODEL", "text-embedding-3-small")
CHAT_MODEL     = os.getenv("CHAT_MODEL", "gpt-4o-mini")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
VECTOR_DB_PATH = str(BASE_DIR.parent / "my_vector_db")

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "money_psychology_docs"