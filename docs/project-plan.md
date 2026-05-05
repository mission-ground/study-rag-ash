# RAG 설계 의사결정 도구 개발 계획

## 1. 프로젝트 목표 요약

이 프로젝트의 목표는 단순히 RAG 파이프라인을 실행하는 것이 아니라, RAG를 설계할 때 각 단계에서 어떤 선택을 해야 하는지 판단하고 학습할 수 있는 도구를 만드는 것이다.

사용자는 문서, 질문 세트, 단계별 전략을 입력하고 다음을 확인할 수 있어야 한다.

- 각 단계에서 어떤 작업이 수행되었는지
- 전략별 중간 산출물이 어떻게 다른지
- 어떤 전략이 정량 지표상 더 나은지
- 왜 해당 전략이 더 적합하다고 볼 수 있는지
- 전체 파이프라인 조합에서는 어떤 설정이 가장 좋은지

따라서 이 프로젝트의 정체성은 `RAG 실행 앱`이 아니라 `RAG 설계 의사결정 학습 도구`이다.

## 2. 프로젝트 정체성

일반적인 RAG 앱은 사용자의 질문에 답하는 것을 목표로 한다. 이 프로젝트는 답변 자체보다 답변이 만들어지는 과정과 설계 판단을 드러내는 것을 목표로 한다.

핵심 질문은 다음과 같다.

- 전처리 단계에서는 어떤 정제가 검색 품질에 도움이 되는가?
- 청킹 단계에서는 어떤 단위와 크기가 문맥 보존에 유리한가?
- 임베딩 단계에서는 어떤 모델이 현재 문서와 질문에 적합한가?
- 검색 단계에서는 어떤 top-k, 검색 방식, 필터링 방식이 좋은 후보를 잘 찾는가?
- 생성 단계에서는 어떤 모델, 파라미터, 프롬프트가 근거에 충실한 답변을 만드는가?
- 특정 설정이 좋은 이유를 지표와 중간 산출물로 설명할 수 있는가?

이 도구는 최종적으로 다음 흐름을 제공해야 한다.

```text
문서 입력
-> 단계별 전략 실행
-> 중간 산출물 확인
-> 정량 지표 비교
-> 전략별 장단점 설명
-> 전체 파이프라인 추천
```

## 3. MVP 범위

MVP는 전체 RAG 설계 자동화를 한 번에 구현하지 않는다. 첫 버전은 학습 효과가 크고 현재 코드에서 확장하기 쉬운 `청킹`과 `검색 품질 비교`에 집중한다.

MVP에 포함할 기능은 다음과 같다.

- PDF 1개 기준 실험
- 현재 PDF 추출 로직 사용
- 기본 전처리 1개
- 청킹 전략 3개 비교
- 현재 SentenceTransformer 임베딩 사용
- ChromaDB 검색 사용
- `top_k`별 검색 결과 비교
- 질문 세트 기반 `recall@k` 계산
- Streamlit에서 단계별 결과 비교
- 청킹과 검색 전략에 대한 간단한 explanation 제공

## 4. MVP 제외 범위

다음 기능은 MVP 이후 단계로 둔다.

- 실제 LLM 생성 품질 평가
- 여러 LLM 모델 비교
- OpenAI API 연동
- reranker 모델 연동
- hybrid search
- query rewrite, multi-query, HyDE
- 비용 계산 고도화
- 대규모 실험 자동화
- 실험 결과 대시보드 고도화

## 5. RAG 단계 세분화

학습용 도구에서는 RAG 단계를 크게 묶기보다 세부 단계로 나누는 것이 좋다. 각 단계가 독립적인 실험 공간이 되어야 사용자가 어떤 선택이 어떤 결과를 만드는지 이해할 수 있다.

권장 단계는 다음과 같다.

1. 문서 파싱
2. 전처리
3. 메타데이터 추출
4. 청킹
5. 임베딩
6. 인덱싱
7. 쿼리 처리
8. 검색
9. 재순위화
10. 컨텍스트 구성
11. 생성
12. 후처리
13. 평가
14. 추천 및 설명

MVP에서는 이 중 `문서 파싱`, `전처리`, `청킹`, `임베딩`, `인덱싱`, `검색`, `평가`, `설명`만 최소 범위로 다룬다.

## 6. 전체 기능 목록

### 6.1 문서 입력 및 파싱

- PDF, TXT, Markdown 등 문서 입력
- 원본 텍스트 추출
- 페이지 단위 정보 유지
- 추출 품질 확인

### 6.2 전처리 Lab

- 공백 제거
- 빈 줄 제거
- 헤더/푸터 제거
- 중복 문장 제거
- 깨진 문자 정리
- 문단 복원
- 원본과 전처리 결과 비교

### 6.3 청킹 Lab

- 고정 문자 길이 청킹
- 토큰 기반 청킹
- 문단 기반 청킹
- 제목/섹션 기반 청킹
- overlap 변경 실험
- chunk 길이, 개수, 절단 의심 비율 비교

### 6.4 임베딩 Lab

- 임베딩 모델별 결과 비교
- embedding dimension 확인
- 처리 시간 비교
- 한국어 질의 검색 품질 비교
- 모델별 장단점 설명

### 6.5 인덱싱 Lab

- ChromaDB 저장
- FAISS 저장
- 인덱싱 시간 비교
- 저장된 chunk 수 확인
- 컬렉션 초기화와 재색인

### 6.6 검색 Lab

- dense search
- top-k 비교
- score threshold 비교
- metadata filter
- query rewrite
- multi-query
- hybrid search
- 검색 결과와 기대 근거 비교

### 6.7 Reranking / Context 구성 Lab

- reranker 미사용
- cross-encoder reranker
- LLM 기반 reranking
- 중복 chunk 제거
- context compression
- 최종 prompt context 구성 방식 비교

### 6.8 생성 Lab

- 모델별 답변 비교
- temperature 변경
- max tokens 변경
- system prompt 비교
- citation prompt 비교
- hallucination 방지 prompt 비교
- 근거 충실도 평가

### 6.9 평가 및 추천

- retrieval recall@k
- precision@k
- MRR
- nDCG
- answer relevance
- faithfulness
- latency
- 비용 추정
- 단계별 추천 이유 설명
- 전체 파이프라인 추천 리포트

## 7. 추천 아키텍처 개념

각 RAG 단계는 교체 가능한 전략으로 구성한다.

```text
Stage
-> Strategy
-> StageResult
```

### 7.1 Stage

`Stage`는 RAG의 한 단계를 의미한다.

예시는 다음과 같다.

- preprocessing
- chunking
- embedding
- retrieval
- reranking
- generation
- evaluation

### 7.2 Strategy

`Strategy`는 같은 단계를 수행하는 여러 방식 중 하나이다.

예시는 다음과 같다.

- token chunking
- paragraph chunking
- dense retrieval
- hybrid retrieval
- citation prompt generation

### 7.3 StageResult

`StageResult`는 각 단계의 실행 결과를 공통 형식으로 담는다.

초기 구조는 다음과 같이 단순하게 시작한다.

```text
StageResult
- stage_name
- strategy_name
- input_summary
- output_summary
- artifacts
- metrics
- observations
- explanation
```

### 7.4 ExperimentResult

`ExperimentResult`는 하나의 실험 실행 결과를 담는다.

```text
ExperimentResult
- experiment_id
- config
- stage_results
- final_metrics
- recommendation
```

## 8. 개발 순서

개발은 작고 검증 가능한 단위로 진행한다.

1. 실험 결과 공통 데이터 구조 정의
2. 평가 질문 세트 구조 정의
3. 샘플 평가 질문 JSON 추가
4. 청킹 전략 인터페이스 정의
5. 기존 토큰 기반 청킹을 전략 구조로 래핑
6. 고정 문자 길이 청킹 구현
7. 문단 기반 청킹 구현
8. 청킹 metric 계산 구현
9. 청킹 실험 runner 구현
10. 서비스 계층에 청킹 실험 연결
11. 청킹 실험 API 추가
12. Streamlit Chunking Lab 추가
13. 검색 평가 metric 구현
14. 검색 실험 runner 구현
15. Streamlit Retrieval Lab 추가
16. 단계별 explanation 규칙 구현
17. Chunking Lab에 explanation 표시
18. Retrieval Lab에 explanation 표시
19. 실험 결과 저장소 구현
20. 실험 히스토리 UI 추가
21. 생성 단계 설정 구조 정리
22. Prompt Lab 초안 구현
23. 전체 PipelineConfig 실행기 구현
24. 전체 추천 리포트 생성

## 9. 단계별 판단 기준

### 9.1 전처리

전처리의 판단 기준은 의미 보존과 노이즈 감소이다.

- 의미 있는 문장이 보존되었는가?
- 헤더, 푸터, 페이지 번호 등 검색 방해 요소가 줄었는가?
- 문단 구조가 망가지지 않았는가?
- 깨진 문자나 불필요한 특수문자가 줄었는가?

### 9.2 청킹

청킹의 판단 기준은 문맥 보존과 검색 가능성이다.

- chunk 안에 충분한 문맥이 포함되는가?
- chunk가 너무 길거나 짧지 않은가?
- 문장이 중간에 잘리는 경우가 적은가?
- 질문에 필요한 근거가 하나 이상의 chunk에 잘 포함되는가?
- overlap이 과도해서 중복이 많아지지 않는가?

### 9.3 임베딩

임베딩의 판단 기준은 의미 유사도 표현력과 운영 비용이다.

- 한국어 질문과 문서를 잘 연결하는가?
- 의미가 유사한 chunk를 가깝게 찾는가?
- 처리 시간이 적절한가?
- 비용과 성능의 균형이 맞는가?

### 9.4 검색

검색의 판단 기준은 정답 근거 회수 능력이다.

- 기대 근거가 top-k 안에 포함되는가?
- 관련 없는 chunk가 상위에 많이 섞이지 않는가?
- 질문 유형에 따라 안정적인 결과를 내는가?
- 생성 단계에 넘길 context로 적합한가?

### 9.5 생성

생성의 판단 기준은 근거 충실도와 답변 품질이다.

- 검색된 근거에 충실하게 답변하는가?
- 질문에 직접 답하는가?
- 없는 내용을 지어내지 않는가?
- 출처를 잘 표시하는가?
- 답변 형식이 안정적인가?

## 10. 리스크와 운영 원칙

### 10.1 주요 리스크

- 처음부터 전체 RAG 자동화로 범위가 커질 수 있다.
- 실험 결과 구조를 너무 복잡하게 만들면 개발 속도가 느려질 수 있다.
- 평가 데이터셋이 없으면 성능 판단이 주관적일 수 있다.
- explanation이 실제 지표와 연결되지 않으면 학습 도구로서 신뢰도가 떨어진다.
- Streamlit 서비스 계층이 비대해질 수 있다.

### 10.2 운영 원칙

- MVP에서는 청킹과 검색 품질 비교에 집중한다.
- 각 작업은 30~90분 안에 끝낼 수 있는 크기로 나눈다.
- 모든 단계는 중간 산출물을 남긴다.
- 추천은 반드시 metric과 observation에 근거해야 한다.
- 새로운 전략은 기존 전략과 같은 인터페이스로 추가한다.
- 전체 파이프라인 자동화보다 단계별 학습 가능성을 우선한다.
