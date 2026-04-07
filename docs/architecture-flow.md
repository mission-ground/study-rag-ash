# RAG Flow Overview

이 문서는 현재 프로젝트에서 RAG가 어떤 구조로 동작하는지 빠르게 파악하기 위한 흐름 정리 문서입니다.

## 1. 전체 구조

현재 구조는 크게 3층으로 나뉩니다.

1. 인터페이스 레이어
- FastAPI: HTTP 요청을 받습니다.
- Streamlit: 사람이 단계별 결과를 직접 확인합니다.

2. 앱 서비스 레이어
- `app/services/rag_app_service.py`
- FastAPI와 Streamlit이 공통으로 사용하는 진입점입니다.
- 기존 RAG 모듈을 조합해서 `preview`, `ingest`, `search`, `ask` 기능을 제공합니다.

3. 기존 RAG 레이어
- `rag/ingestion/*`
- `rag/retrieval/*`
- `rag/generation/*`
- `rag/components/*`
- `rag/rag_pipeline.py`

즉, FastAPI와 Streamlit은 직접 세부 로직을 구현하지 않고 `RAGAppService`를 호출하고, 실제 처리는 기존 `rag` 구조가 담당합니다.

## 2. 진입점

### FastAPI

- 파일: `main.py`
- 라우터: `api/routes/chat.py`

FastAPI는 아래 엔드포인트를 제공합니다.

- `GET /api/chat/health`
- `POST /api/chat/preview`
- `POST /api/chat/ingest`
- `POST /api/chat/search`
- `POST /api/chat/ask`

### Streamlit

- 파일: `streamlit_app.py`

Streamlit은 디버그용 UI 역할을 하며 다음을 확인할 수 있습니다.

- PDF 원문 추출 결과
- 문서 분리 결과
- 청크 결과
- 임베딩 일부 값
- 검색 결과와 raw 응답

## 3. 공통 서비스 흐름

FastAPI와 Streamlit은 둘 다 아래 함수를 통해 같은 서비스 인스턴스를 사용합니다.

- 파일: `api/dependencies.py`
- 함수: `get_rag_service()`

이 함수는 `RAGAppService`를 캐시해서 매 요청마다 모델과 벡터 스토어를 다시 만들지 않도록 합니다.

## 4. Ingest 흐름

적재 흐름은 아래 순서로 진행됩니다.

1. 인터페이스 레이어에서 `RAGAppService.ingest_pdf()` 호출
2. `build_ingest_preview()`로 중간 결과 생성
3. PDF 텍스트 추출
4. 문서 분리
5. 문서 청킹
6. 청크 임베딩 생성
7. Chroma 벡터 DB에 저장

관련 파일은 다음과 같습니다.

- `app/services/rag_app_service.py`
- `rag/ingestion/document_processor.py`
- `rag/ingestion/pdf_extractor.py`
- `rag/ingestion/chunker.py`
- `rag/components/embedding/sentence_transformer_embedder.py`
- `rag/components/vectorstore/chroma/chroma_store.py`

흐름을 간단히 쓰면:

```text
PDF
 -> extract_text()
 -> split_documents()
 -> chunk_documents()
 -> embed_documents()
 -> add_documents()
```

## 5. Preview 흐름

`preview`는 실제 저장 없이 중간 결과만 확인하는 흐름입니다.

사용 목적:

- PDF 추출이 제대로 되는지 확인
- 공백 줄이 제거되는지 확인
- chunk 크기가 적절한지 확인
- 임베딩 차원이 정상인지 확인

흐름은 다음과 같습니다.

```text
PDF
 -> raw text
 -> documents
 -> chunks
 -> embeddings preview
```

이 기능은 Streamlit의 Ingestion 탭과 FastAPI의 `POST /api/chat/preview`에서 같이 사용합니다.

## 6. Search 흐름

검색 흐름은 아래 순서로 진행됩니다.

1. 질문 입력
2. 질문 임베딩 생성
3. Chroma에서 유사도 검색
4. 문서/거리/ID 정리
5. API 또는 UI에 결과 반환

관련 파일:

- `app/services/rag_app_service.py`
- `rag/components/embedding/sentence_transformer_embedder.py`
- `rag/components/vectorstore/chroma/chroma_store.py`

흐름을 간단히 쓰면:

```text
query
 -> embed_query()
 -> vectorstore.query()
 -> ranked items
```

## 7. Ask 흐름

`ask`는 예전 RAG 파이프라인을 그대로 이용하는 엔드투엔드 흐름입니다.

관련 파일:

- `app/services/rag_app_service.py`
- `rag/rag_pipeline.py`
- `rag/retrieval/retriever.py`
- `rag/generation/generator.py`

흐름은 다음과 같습니다.

```text
query
 -> Retriever.retrieve()
 -> relevant documents
 -> Generator.generate()
 -> answer
```

즉 `ask`는 기존 구조를 유지하기 위한 경로이고, `search`는 검색 결과를 디버깅하기 위한 경로입니다.

## 8. 역할 분리 기준

현재 구조는 아래 기준으로 분리되어 있습니다.

- `api/`
  HTTP 인터페이스

- `streamlit_app.py`
  사람이 확인하는 디버그 UI

- `app/services/`
  인터페이스 레이어와 RAG 레이어를 연결하는 조합 지점

- `rag/`
  실제 RAG 처리 로직

- `core/config.py`
  경로, 모델명, 컬렉션명 같은 설정값

## 9. 파일별 핵심 역할

- `main.py`
  FastAPI 앱 실행 진입점

- `streamlit_app.py`
  단계별 점검용 UI

- `api/routes/chat.py`
  preview / ingest / search / ask 엔드포인트 정의

- `api/dependencies.py`
  공통 서비스 생성 및 캐시

- `app/services/rag_app_service.py`
  앱 관점의 통합 서비스

- `rag/ingestion/document_processor.py`
  추출 텍스트 정리 및 청킹

- `rag/retrieval/retriever.py`
  쿼리 벡터화 및 검색 연결

- `rag/rag_pipeline.py`
  검색 + 생성 파이프라인

- `rag/components/vectorstore/chroma/chroma_store.py`
  Chroma 저장/조회 처리

## 10. 확인 포인트

문제가 생겼을 때는 보통 아래 순서로 보면 됩니다.

1. PDF 추출 결과가 비정상인지
2. 문서 분리 결과에 공백이나 이상한 텍스트가 많은지
3. chunk가 너무 짧거나 너무 긴지
4. vector store에 정상 저장됐는지
5. 검색 결과의 거리값과 문서가 적절한지
6. `ask` 단계에서 생성기가 예상대로 동작하는지

이 문서를 기준으로 보면 어느 파일에서 어떤 책임을 가지는지 빠르게 추적할 수 있습니다.
