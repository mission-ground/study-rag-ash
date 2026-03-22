from core.config import PDF_PATH
from rag.retrieval.query_service import RAGQueryService


def main():
    file_path = PDF_PATH
    query = "복리란 무엇인가 복리란 무엇인가 복리란 무엇인가 복리란 무엇인가"

    rag_service = RAGQueryService()

    rag_service.ingest_pdf(file_path=file_path)
    results = rag_service.search(query=query, n_results=3)

    print("\n--- [검색 결과] ---")
    for i, doc in enumerate(results["documents"][0]):
        print(f"{i + 1}번째 관련 문장: {doc}")


if __name__ == "__main__":
    main()
