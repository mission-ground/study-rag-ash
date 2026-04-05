import argparse

from core.config import PDF_PATH
from rag.retrieval.query_service import RAGQueryService


def parse_args():
    parser = argparse.ArgumentParser(description="RAG PDF search runner")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Rebuild or initialize the vector store from the source PDF before searching.",
    )
    parser.add_argument(
        "--pdf-path",
        default=PDF_PATH,
        help="PDF file path to ingest when --ingest is used.",
    )
    parser.add_argument(
        "--query",
        default="이 책에서 말하는 돈 관리의 핵심은 무엇인가요?",
        help="Question to search against the vector store.",
    )
    parser.add_argument(
        "--n-results",
        type=int,
        default=3,
        help="Number of search results to return.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    rag_service = RAGQueryService()

    if args.ingest:
        rag_service.ingest_pdf(file_path=args.pdf_path)

    results = rag_service.search(query=args.query, n_results=args.n_results)

    print("\n--- [검색 결과] ---")
    for i, doc in enumerate(results["documents"][0]):
        print(f"{i + 1}번째 관련 문장: {doc}")


if __name__ == "__main__":
    main()
