import chromadb
import fitz
from sentence_transformers import SentenceTransformer

from core.config import COLLECTION_NAME, PDF_PATH, VECTOR_DB_PATH


def extract_korean_english_text(file_path):
    text_data = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text_data += page.get_text("text", sort=True) + "\n"
    return text_data


pdf_text = extract_korean_english_text(PDF_PATH)
print(pdf_text)

documents = pdf_text.split("\n")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(documents)
print(type(embeddings), len(embeddings))

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)
ids = [f"doc_{i}" for i in range(len(documents))]

if collection.count() == 0:
    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        ids=ids,
    )
    print(f"총 {collection.count()}개의 데이터가 벡터 DB에 성공적으로 저장되었습니다!")
else:
    print(f"이미 {collection.count()}개의 데이터가 벡터 DB에 저장되어 있습니다!")

query = "이 책에서 말하는 돈 관리의 핵심은 무엇인가요?"
query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
)

print("\n--- [검색 결과] ---")
for i, doc in enumerate(results["documents"][0]):
    print(f"{i + 1}번째 관련 문장: {doc}")
