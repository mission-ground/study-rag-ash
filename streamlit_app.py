from pathlib import Path

import streamlit as st

from api.dependencies import get_rag_service
from core.config import PDF_PATH

st.set_page_config(
    page_title="RAG Inspector",
    page_icon="R",
    layout="wide",
)


def default_pdf_path():
    return str(Path(PDF_PATH))


def render_ingest_tab():
    st.subheader("Ingestion Inspector")
    st.caption(
        "Inspect each ingestion stage: PDF extraction, document splitting, chunking, embeddings, and vector store updates."
    )

    rag_service = get_rag_service()
    pdf_path = st.text_input("PDF path", value=default_pdf_path())
    preview_clicked = st.button("Generate preview", use_container_width=True)

    if preview_clicked:
        with st.spinner("Analyzing PDF..."):
            preview = rag_service.build_ingest_preview(pdf_path)

        st.success("Preview generated.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Documents", preview["document_count"])
        col2.metric("Chunks", preview["chunk_count"])
        col3.metric("Embedding dim", preview["embedding_dimension"])
        col4.metric("Vector store items", preview["vector_store_count"])

        with st.expander("1. Raw text preview", expanded=True):
            st.text_area(
                "Extracted text",
                value=preview["raw_text"][:5000],
                height=220,
            )

        with st.expander("2. Document split preview", expanded=True):
            rows = [
                {"index": idx + 1, "text": doc}
                for idx, doc in enumerate(preview["documents"][:30])
            ]
            if rows:
                st.dataframe(rows, use_container_width=True)
            else:
                st.info("No documents were extracted.")

        with st.expander("3. Chunk preview", expanded=True):
            rows = [
                {"index": idx + 1, "chunk": chunk}
                for idx, chunk in enumerate(preview["chunks"][:30])
            ]
            if rows:
                st.dataframe(rows, use_container_width=True)
            else:
                st.info("No chunks were produced.")

        with st.expander("4. Embedding preview", expanded=True):
            st.write(
                {
                    "embedding_dimension": preview["embedding_dimension"],
                    "sample_embedding_first_8": preview["sample_embedding"],
                }
            )

    st.divider()
    st.subheader("Index Control")
    reset_before_ingest = st.checkbox("Reset collection before ingest", value=False)

    if st.button("Ingest into vector store", type="primary", use_container_width=True):
        with st.spinner("Writing chunks into the vector store..."):
            result = rag_service.ingest_pdf(pdf_path, reset=reset_before_ingest)
        st.write(result)


def render_search_tab():
    st.subheader("Retrieval Inspector")
    st.caption(
        "Inspect query embeddings, ranked retrieval results, and raw vector store responses."
    )

    rag_service = get_rag_service()
    query = st.text_area(
        "Query",
        value="What is the core money management lesson in this book?",
        height=100,
    )
    n_results = st.slider("Number of results", min_value=1, max_value=10, value=3)

    if st.button("Run search", type="primary", use_container_width=True):
        with st.spinner("Searching the vector store..."):
            result = rag_service.search(query=query, n_results=n_results)

        col1, col2 = st.columns(2)
        col1.metric("Query embedding dim", result["query_embedding_dimension"])
        col2.metric("Returned items", len(result["items"]))

        with st.expander("1. Query embedding preview", expanded=True):
            st.write({"query_embedding_first_8": result["query_embedding_preview"]})

        with st.expander("2. Retrieval results", expanded=True):
            if result["items"]:
                st.dataframe(result["items"], use_container_width=True)
            else:
                st.info("No results found. Run ingest first.")

        with st.expander("3. Raw vector store response", expanded=False):
            st.json(result["raw"])


def main():
    st.title("RAG Step Inspector")
    st.caption(
        "Use this UI to validate each RAG stage and quickly find where the pipeline starts to drift."
    )

    ingest_tab, search_tab = st.tabs(["Ingestion", "Retrieval"])

    with ingest_tab:
        render_ingest_tab()

    with search_tab:
        render_search_tab()


if __name__ == "__main__":
    main()
