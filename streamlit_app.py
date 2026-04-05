from pathlib import Path

import streamlit as st

from core.config import PDF_PATH
from rag.retrieval.query_service import RAGQueryService

st.set_page_config(
    page_title="RAG Inspector",
    page_icon="🔎",
    layout="wide",
)


@st.cache_resource
def get_rag_service():
    return RAGQueryService()


def default_pdf_path():
    return str(Path(PDF_PATH))


def render_ingest_tab(rag_service: RAGQueryService):
    st.subheader("Ingestion Inspector")
    st.caption("PDF 추출, 문서 분리, 임베딩 생성, 벡터 DB 적재 상태를 단계별로 확인합니다.")

    pdf_path = st.text_input("PDF 경로", value=default_pdf_path())
    preview_clicked = st.button("추출/임베딩 미리보기", use_container_width=True)

    if preview_clicked:
        with st.spinner("PDF를 분석하고 있습니다..."):
            preview = rag_service.preview_ingest(pdf_path)

        st.success("미리보기를 생성했습니다.")

        col1, col2, col3 = st.columns(3)
        col1.metric("추출 문서 수", preview["document_count"])
        col2.metric("임베딩 차원", preview["embedding_dimension"])
        col3.metric("현재 벡터 DB 수", preview["vector_store_count"])

        with st.expander("1. Raw Text Preview", expanded=True):
            st.text_area(
                "PDF에서 추출한 원문",
                value=preview["raw_text"][:5000],
                height=240,
            )

        with st.expander("2. Split Documents Preview", expanded=True):
            if preview["documents"]:
                rows = [
                    {"index": idx + 1, "text": doc}
                    for idx, doc in enumerate(preview["documents"][:30])
                ]
                st.dataframe(rows, use_container_width=True)
            else:
                st.info("추출된 문서가 없습니다.")

        with st.expander("3. Embedding Preview", expanded=True):
            st.write(
                {
                    "embedding_dimension": preview["embedding_dimension"],
                    "sample_embedding_first_8": preview["sample_embedding"],
                }
            )

    st.divider()
    st.subheader("Index Control")
    reset_before_ingest = st.checkbox("기존 컬렉션을 초기화하고 다시 적재", value=False)

    if st.button("벡터 DB에 적재", type="primary", use_container_width=True):
        with st.spinner("벡터 DB에 적재하고 있습니다..."):
            result = rag_service.ingest_pdf(pdf_path, reset=reset_before_ingest)
        st.write(result)


def render_search_tab(rag_service: RAGQueryService):
    st.subheader("Retrieval Inspector")
    st.caption("질문 임베딩, 검색 결과, 거리값, raw 응답을 단계별로 확인합니다.")

    query = st.text_area(
        "질문",
        value="이 책에서 말하는 돈 관리의 핵심은 무엇인가요?",
        height=100,
    )
    n_results = st.slider("검색 개수", min_value=1, max_value=10, value=3)

    if st.button("검색 실행", type="primary", use_container_width=True):
        with st.spinner("질문을 검색하고 있습니다..."):
            result = rag_service.search(query=query, n_results=n_results)

        col1, col2 = st.columns(2)
        col1.metric("질문 임베딩 차원", result["query_embedding_dimension"])
        col2.metric("반환 문서 수", len(result["items"]))

        with st.expander("1. Query Embedding Preview", expanded=True):
            st.write({"query_embedding_first_8": result["query_embedding_preview"]})

        with st.expander("2. Retrieval Results", expanded=True):
            if result["items"]:
                st.dataframe(result["items"], use_container_width=True)
            else:
                st.info("검색 결과가 없습니다. 먼저 ingest를 수행해 주세요.")

        with st.expander("3. Raw Vector Store Response", expanded=False):
            st.json(result["raw"])


def main():
    st.title("RAG Step Inspector")
    st.caption("RAG 파이프라인의 각 단계를 직접 확인하면서 문제 지점을 찾기 위한 Streamlit UI")

    rag_service = get_rag_service()
    ingest_tab, search_tab = st.tabs(["Ingestion", "Retrieval"])

    with ingest_tab:
        render_ingest_tab(rag_service)

    with search_tab:
        render_search_tab(rag_service)


if __name__ == "__main__":
    main()
