# RAG 설계 의사결정 도구 작업 티켓

## 작업 단위 원칙

- 한 작업은 가능하면 30~90분 안에 끝낼 수 있는 크기로 나눈다.
- 한 티켓은 하나의 명확한 목적을 가진다.
- 선행 작업이 끝나지 않으면 의존 티켓을 시작하지 않는다.
- MVP에서는 청킹과 검색 품질 비교를 우선한다.
- 생성 모델 비교, reranking, hybrid search, 비용 계산 고도화는 MVP 이후로 둔다.

## 가장 먼저 수행할 작업

가장 먼저 수행할 작업은 `TASK-001`이다.

`TASK-001`은 이후 모든 단계별 실험 결과가 공통으로 사용할 데이터 구조를 정의하는 작업이다. 청킹, 검색, 생성, 평가, 추천 기능이 모두 이 구조를 기준으로 확장되므로 먼저 기준점을 잡는 것이 좋다.

## TASK-001 수행 전 확인 리스크

- 데이터 구조를 너무 복잡하게 만들면 MVP 개발 속도가 느려질 수 있다.
- 데이터 구조를 너무 단순하게 만들면 나중에 생성, reranking, 전체 파이프라인 평가를 붙일 때 다시 수정 범위가 커질 수 있다.
- `metrics`와 `artifacts`를 어디까지 공통화할지 정해야 한다.
- Streamlit 표시용 구조와 내부 저장용 구조를 완전히 같게 할지, 일부 분리할지 결정해야 한다.
- Pydantic 모델을 쓸지 dataclass를 쓸지 정해야 한다.
- 실험 결과를 즉시 파일로 저장할지, MVP에서는 메모리 반환만 할지 정해야 한다.
- 현재 `RAGAppService`에 책임이 집중되어 있어 실험 기능을 무리하게 붙이면 서비스가 비대해질 수 있다.

초기 추천은 Pydantic 기반의 얇은 공통 모델만 정의하고, 저장소와 추천 엔진은 뒤 티켓으로 미루는 것이다.

## 작업 목록

### TASK-001: 실험 결과 공통 데이터 구조 정의

- 목적: 모든 RAG 단계 실험 결과를 같은 형식으로 다루기 위한 공통 모델을 정의한다.
- 수정 예상 파일: `rag/experiments/models.py`
- 선행 작업: 없음
- 완료 기준:
  - `StageResult` 구조가 정의되어 있다.
  - `ExperimentConfig` 구조가 정의되어 있다.
  - `ExperimentResult` 구조가 정의되어 있다.
  - 각 모델은 stage name, strategy name, metrics, artifacts, explanation을 담을 수 있다.

### TASK-002: 평가 질문 세트 구조 정의

- 목적: 검색과 생성 품질을 평가하기 위한 질문 데이터 모델을 정의한다.
- 수정 예상 파일: `rag/evaluation/dataset.py`
- 선행 작업: `TASK-001`
- 완료 기준:
  - 질문, 기대 답변, 기대 근거, 출처 정보를 담는 구조가 정의되어 있다.
  - 질문 난이도와 질문 유형을 담을 수 있다.
  - JSON 파일에서 평가 질문을 로드할 수 있는 함수 초안이 있다.

### TASK-003: 샘플 평가 질문 JSON 추가

- 목적: 현재 PDF를 기준으로 MVP 실험에 사용할 작은 평가 질문 세트를 만든다.
- 수정 예상 파일: `docs/evaluation_questions.json`
- 선행 작업: `TASK-002`
- 완료 기준:
  - 질문 5~10개가 등록되어 있다.
  - 각 질문에 기대 답변 또는 기대 근거가 포함되어 있다.
  - 검색 평가에 사용할 수 있는 최소 근거 텍스트가 포함되어 있다.

### TASK-004: 청킹 전략 인터페이스 정의

- 목적: 여러 청킹 방식을 같은 방식으로 실행할 수 있도록 공통 인터페이스를 정의한다.
- 수정 예상 파일: `rag/stages/chunking/base.py`
- 선행 작업: `TASK-001`
- 완료 기준:
  - 청킹 전략의 입력과 출력 형식이 정의되어 있다.
  - strategy name을 반환할 수 있다.
  - 이후 청킹 전략들이 같은 인터페이스를 따를 수 있다.

### TASK-005: 기존 토큰 기반 청킹을 전략으로 래핑

- 목적: 현재 `Chunker`의 토큰 기반 청킹을 새 전략 구조에서 실행할 수 있게 한다.
- 수정 예상 파일: `rag/stages/chunking/token_chunker.py`, `rag/ingestion/chunker.py`
- 선행 작업: `TASK-004`
- 완료 기준:
  - 기존 토큰 기반 청킹이 strategy 형태로 실행된다.
  - 기존 RAG 흐름이 깨지지 않는다.
  - chunk size와 overlap 설정을 받을 수 있다.

### TASK-006: 고정 문자 길이 청킹 구현

- 목적: 단순한 기준 전략으로 사용할 character 기반 청킹을 구현한다.
- 수정 예상 파일: `rag/stages/chunking/character_chunker.py`
- 선행 작업: `TASK-004`
- 완료 기준:
  - `chunk_size`와 `overlap`을 설정할 수 있다.
  - 문자열 길이 기준으로 chunk가 생성된다.
  - 빈 chunk가 생성되지 않는다.

### TASK-007: 문단 기반 청킹 구현

- 목적: 문맥 보존 관점에서 비교할 paragraph 기반 청킹을 구현한다.
- 수정 예상 파일: `rag/stages/chunking/paragraph_chunker.py`
- 선행 작업: `TASK-004`
- 완료 기준:
  - 빈 줄 또는 문단 구분 기준으로 chunk가 생성된다.
  - 너무 긴 문단은 설정된 최대 길이에 맞게 분리된다.
  - 문단 단위 보존 여부를 metric에서 확인할 수 있다.

### TASK-008: 청킹 metric 계산 구현

- 목적: 청킹 결과를 정량적으로 비교하기 위한 기본 지표를 계산한다.
- 수정 예상 파일: `rag/evaluation/chunking_metrics.py`
- 선행 작업: `TASK-005`, `TASK-006`, `TASK-007`
- 완료 기준:
  - chunk 개수를 계산한다.
  - 평균, 최소, 최대 chunk 길이를 계산한다.
  - 빈 chunk 수를 계산한다.
  - 문장 절단 의심 비율을 계산한다.
  - 중복 또는 overlap 비율을 계산할 수 있는 초안이 있다.

### TASK-009: 청킹 실험 runner 구현

- 목적: 여러 청킹 전략을 한 번에 실행하고 비교 결과를 반환한다.
- 수정 예상 파일: `rag/experiments/chunking_runner.py`
- 선행 작업: `TASK-008`
- 완료 기준:
  - 여러 전략 목록을 입력받아 순차 실행할 수 있다.
  - 각 전략의 결과가 `StageResult`로 반환된다.
  - metric과 sample artifacts가 포함된다.

### TASK-010: 서비스 계층에 청킹 실험 메서드 추가

- 목적: API와 Streamlit에서 청킹 실험 기능을 호출할 수 있게 한다.
- 수정 예상 파일: `app/services/rag_app_service.py`
- 선행 작업: `TASK-009`
- 완료 기준:
  - `RAGAppService`에서 청킹 비교 메서드를 제공한다.
  - PDF 경로를 입력받아 텍스트 추출 후 청킹 실험을 실행한다.
  - 반환 결과가 UI에서 바로 표시 가능한 형태이다.

### TASK-011: 청킹 실험 API 추가

- 목적: HTTP API로 청킹 실험을 실행할 수 있게 한다.
- 수정 예상 파일: `api/routes/chat.py` 또는 `api/routes/experiments.py`
- 선행 작업: `TASK-010`
- 완료 기준:
  - 청킹 실험 요청 모델이 정의되어 있다.
  - PDF 경로와 전략 설정을 입력받을 수 있다.
  - 실행 결과를 JSON으로 반환한다.

### TASK-012: Streamlit Chunking Lab 추가

- 목적: 사용자가 UI에서 청킹 전략별 결과를 비교할 수 있게 한다.
- 수정 예상 파일: `streamlit_app.py`
- 선행 작업: `TASK-010`
- 완료 기준:
  - Chunking Lab 탭 또는 섹션이 추가되어 있다.
  - 전략별 chunk metric이 표시된다.
  - 전략별 sample chunk가 표시된다.
  - 사용자가 chunk size, overlap을 조정할 수 있다.

### TASK-013: 검색 평가 metric 구현

- 목적: 검색 결과가 기대 근거를 얼마나 잘 찾는지 계산한다.
- 수정 예상 파일: `rag/evaluation/retrieval_metrics.py`
- 선행 작업: `TASK-002`
- 완료 기준:
  - `recall@k`를 계산할 수 있다.
  - `precision@k`를 계산할 수 있다.
  - 질문별 검색 성공 여부를 반환할 수 있다.

### TASK-014: 검색 실험 runner 구현

- 목적: 질문 세트 기준으로 검색 설정을 평가한다.
- 수정 예상 파일: `rag/experiments/retrieval_runner.py`
- 선행 작업: `TASK-013`
- 완료 기준:
  - 질문 세트를 순회하며 검색을 실행한다.
  - top-k 설정별 결과를 비교할 수 있다.
  - 결과가 `StageResult` 또는 `ExperimentResult` 형식으로 반환된다.

### TASK-015: Streamlit Retrieval Lab 추가

- 목적: 사용자가 UI에서 검색 결과와 검색 지표를 확인할 수 있게 한다.
- 수정 예상 파일: `streamlit_app.py`
- 선행 작업: `TASK-014`
- 완료 기준:
  - Retrieval Lab 탭 또는 섹션이 추가되어 있다.
  - 질문별 검색 결과가 표시된다.
  - 기대 근거 포함 여부가 표시된다.
  - `recall@k` 결과가 표시된다.

### TASK-016: 단계별 explanation 규칙 구현

- 목적: metric과 observation을 기반으로 왜 특정 전략이 좋은지 설명한다.
- 수정 예상 파일: `rag/evaluation/explanation.py`
- 선행 작업: `TASK-008`, `TASK-013`
- 완료 기준:
  - 청킹 metric 기반 설명을 생성한다.
  - 검색 metric 기반 설명을 생성한다.
  - 장점과 주의점을 함께 반환한다.

### TASK-017: Chunking Lab에 explanation 표시

- 목적: 청킹 실험 결과에 학습용 설명을 붙인다.
- 수정 예상 파일: `streamlit_app.py`
- 선행 작업: `TASK-016`
- 완료 기준:
  - 전략별 설명이 UI에 표시된다.
  - 가장 추천되는 청킹 전략이 표시된다.
  - 추천 이유가 metric과 연결되어 있다.

### TASK-018: Retrieval Lab에 explanation 표시

- 목적: 검색 실험 결과에 학습용 설명을 붙인다.
- 수정 예상 파일: `streamlit_app.py`
- 선행 작업: `TASK-016`
- 완료 기준:
  - 검색 설정별 설명이 UI에 표시된다.
  - top-k 설정의 장단점이 표시된다.
  - 검색 품질 지표와 설명이 연결되어 있다.

### TASK-019: 실험 결과 저장소 설계

- 목적: 실험 결과를 파일로 저장하고 다시 불러올 수 있게 한다.
- 수정 예상 파일: `rag/experiments/storage.py`
- 선행 작업: `TASK-001`
- 완료 기준:
  - 실험 결과를 JSON으로 저장할 수 있다.
  - 저장된 실험 결과를 불러올 수 있다.
  - 저장 경로를 설정할 수 있다.

### TASK-020: 실험 히스토리 UI 추가

- 목적: 과거 실험 결과를 Streamlit에서 확인할 수 있게 한다.
- 수정 예상 파일: `streamlit_app.py`
- 선행 작업: `TASK-019`
- 완료 기준:
  - 저장된 실험 목록이 표시된다.
  - 선택한 실험 결과를 확인할 수 있다.
  - 이전 실험과 현재 실험을 비교할 수 있는 초안이 있다.

### TASK-021: 생성 단계 실제 구조 정리

- 목적: 현재 stub 형태의 생성 단계를 향후 실제 LLM 연동이 가능한 구조로 정리한다.
- 수정 예상 파일: `rag/generation/generator.py`, `core/config.py`
- 선행 작업: `TASK-001`
- 완료 기준:
  - 모델명, temperature, max tokens, prompt template 설정 구조가 있다.
  - 실제 LLM 호출 전에도 prompt를 확인할 수 있다.
  - 기존 `ask` 흐름이 깨지지 않는다.

### TASK-022: Prompt Lab 초안 구현

- 목적: 생성 단계에서 prompt와 context 구성을 비교할 수 있는 초안 기능을 만든다.
- 수정 예상 파일: `rag/experiments/generation_runner.py`, `streamlit_app.py`
- 선행 작업: `TASK-021`
- 완료 기준:
  - 같은 context에 대해 여러 prompt template을 비교할 수 있다.
  - 최종 prompt가 UI에 표시된다.
  - 답변 생성 전 단계에서도 학습용 비교가 가능하다.

### TASK-023: 전체 PipelineConfig 실행기 구현

- 목적: 하나의 설정으로 전체 RAG 흐름을 실행할 수 있게 한다.
- 수정 예상 파일: `rag/experiments/pipeline_runner.py`
- 선행 작업: `TASK-009`, `TASK-014`, `TASK-021`
- 완료 기준:
  - preprocessing, chunking, embedding, retrieval, generation 설정을 하나의 config로 받을 수 있다.
  - 전체 실행 결과가 `ExperimentResult`로 반환된다.
  - 단계별 결과가 함께 포함된다.

### TASK-024: 전체 추천 리포트 생성

- 목적: 전체 실험 결과를 바탕으로 추천 설정과 이유를 제시한다.
- 수정 예상 파일: `rag/evaluation/recommendation.py`
- 선행 작업: `TASK-023`
- 완료 기준:
  - 전체 점수와 단계별 점수를 요약한다.
  - 추천 설정을 제시한다.
  - 추천 이유, 장점, 주의점을 함께 반환한다.
