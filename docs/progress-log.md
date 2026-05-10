# Progress Log

## 2026-05-10 / Desktop

### 작업 브랜치

docs/rag-plan-by-codex

### 완료한 작업

- project-plan.md 작성
- tasks.md 작성
- commit: 71f1c47 docs: RAG 설계 의사결정 도구 계획 문서 추가

### 현재 상태

- 원격 push 완료
- PR 생성은 GitHub API 권한 문제로 실패
- PR 생성 URL: https://github.com/mission-ground/study-rag-ash/pull/new/docs/rag-plan-by-codex
- 다음 작업은 TASK-001부터 진행 예정

### 다음에 할 일

- TASK-001 상세 계획 확인
- 구현 전 변경 파일 목록 확인
- 실험 결과 공통 데이터 구조 설계 확정

## 2026-05-10 / Desktop / TASK-001

### 작업 브랜치

docs/rag-plan-by-codex

### 완료한 작업

- TASK-001 실험 결과 공통 데이터 구조 정의 진행
- rag/experiments/models.py에 StageResult, ExperimentConfig, ExperimentResult 구조 확인
- 저장소, 평가 질문, 청킹 전략, runner 구현은 TASK-001 범위 밖으로 제외

### 현재 상태

- TASK-001 구현 파일은 rag/experiments/models.py
- 진행 기록은 docs/progress-log.md에 업데이트
- 다음 작업은 TASK-002 준비 또는 TASK-001 커밋 검토

### 다음에 할 일

- TASK-001 변경 범위 확인
- TASK-001 검증 결과 확인
- TASK-002 진행 전 별도 계획 작성

## 2026-05-10 / TASK-001 결과 기록

### 작업 브랜치

docs/rag-plan-by-codex

### 수행한 TASK

- TASK-001: 실험 결과 공통 데이터 구조 정의

### 수정한 파일

- rag/experiments/models.py
- docs/progress-log.md

### 실행한 검증 명령

- `python -c "source = open('rag/experiments/models.py', encoding='utf-8').read(); compile(source, 'rag/experiments/models.py', 'exec'); print('syntax ok')"`
- `$env:PYTHONDONTWRITEBYTECODE='1'; python -c "from rag.experiments.models import StageResult, ExperimentConfig, ExperimentResult; ..."`
- `python -m pip show pydantic`
- `git -c safe.directory=C:/repository/study-rag-ash status --short --branch --untracked-files=all`

### 검증 결과

- 문법 검증은 성공했다.
- import 및 인스턴스 생성 검증은 실패했다.
- 실패 이유는 현재 활성 Python 환경에 pydantic 패키지가 설치되어 있지 않기 때문이다.
- `python -m pip show pydantic` 명령에서도 pydantic 패키지를 찾지 못했다.
- Git 상태 확인 결과 `docs/progress-log.md`는 수정 상태이고 `rag/experiments/models.py`는 신규 untracked 상태이다.

### 커밋 여부

- 아직 커밋하지 않았다.

### 다음에 이어서 할 작업

- TASK-001 변경 범위를 검토한다.
- 필요하면 pydantic이 설치된 프로젝트 환경에서 import 검증을 다시 실행한다.
- TASK-001 변경을 커밋한다.
- TASK-002를 시작하기 전 별도 계획을 작성한다.

### 주의해야 할 점

- TASK-001 범위를 벗어나는 평가 질문, 청킹 전략, runner, 저장소 기능은 아직 구현하지 않았다.
- 현재 환경에서는 pydantic 미설치로 런타임 import 검증이 실패한다.
- `requirements.txt`에는 pydantic이 포함되어 있으므로, 실제 프로젝트 의존성이 설치된 환경에서 재검증이 필요하다.

## 2026-05-11 / TASK-002 결과 기록

### 작업 브랜치

docs/rag-plan-by-codex

### 수행한 TASK

- TASK-002: 평가 질문 세트 구조 정의

### 수정한 파일

- rag/evaluation/dataset.py
- docs/progress-log.md

### 완료한 작업

- EvaluationQuestion 모델 정의
- EvaluationDataset 모델 정의
- JSON 파일에서 평가 질문을 로드하는 load_evaluation_questions 함수 초안 작성
- list 형태 JSON과 questions 필드를 가진 object 형태 JSON을 지원
- Windows 환경에서 생성된 UTF-8 BOM 포함 JSON 파일도 읽을 수 있도록 로더 보완

### 현재 상태

- 실제 샘플 평가 질문 JSON은 TASK-003 범위이므로 생성하지 않았다.
- 검색 metric, retrieval runner, UI 연동은 TASK-013 이후 범위이므로 구현하지 않았다.
- TASK-002 변경사항은 아직 커밋하지 않았다.

### 다음에 할 일

- TASK-002 검증 결과 확인
- TASK-002 변경 범위 검토
- TASK-002 커밋
- TASK-003 진행 전 별도 계획 작성

### 주의해야 할 점

- expected_evidence는 여러 근거 조각을 담을 수 있도록 list[str]로 정의했다.
- JSON 로더는 최소 초안만 구현했으며, 고급 검증이나 자동 정규화는 이후 작업에서 다룬다.

## 2026-05-11 / TASK-002 검증 결과 기록

### 작업 브랜치

docs/rag-plan-by-codex

### 수행한 TASK

- TASK-002: 평가 질문 세트 구조 정의

### 수정한 파일

- rag/evaluation/dataset.py
- docs/progress-log.md

### 실행한 검증 명령

- `C:\Users\d9801\miniconda3\envs\money_rag\python.exe -c "source = open('rag/evaluation/dataset.py', encoding='utf-8').read(); compile(source, 'rag/evaluation/dataset.py', 'exec'); print('syntax ok')"`
- `C:\Users\d9801\miniconda3\envs\money_rag\python.exe -c "from rag.evaluation.dataset import EvaluationQuestion, EvaluationDataset; ..."`
- 임시 list 형태 JSON 파일 생성 후 `load_evaluation_questions` 실행
- 임시 object 형태 JSON 파일 생성 후 `load_evaluation_questions` 실행
- `git -c safe.directory=C:/repository/study-rag-ash status --short --branch --untracked-files=all`

### 검증 결과

- 문법 검증은 성공했다.
- EvaluationQuestion, EvaluationDataset import 및 인스턴스 생성 검증은 성공했다.
- list 형태 JSON 로드 검증은 성공했다.
- object 형태 JSON 로드 검증은 성공했다.
- 검증 중 PowerShell에서 생성한 UTF-8 BOM 포함 JSON을 처음에는 읽지 못했으며, `utf-8-sig`로 로더를 보완한 뒤 성공했다.
- Git 상태 확인 결과 `docs/progress-log.md`는 수정 상태이고 `rag/evaluation/dataset.py`는 신규 untracked 상태이다.

### 커밋 여부

- 아직 커밋하지 않았다.

### 다음에 이어서 할 작업

- TASK-002 변경 범위를 검토한다.
- TASK-002 변경사항을 커밋한다.
- TASK-003 진행 전 별도 계획을 작성한다.

### 주의해야 할 점

- 실제 샘플 평가 질문 JSON 파일은 TASK-003 범위이므로 생성하지 않았다.
- 검색 metric, retrieval runner, UI 연동은 TASK-002 범위가 아니므로 구현하지 않았다.
- JSON 로더는 최소 초안이며, 스키마 고도화나 엄격한 데이터 검증은 이후 작업에서 다룬다.

## 2026-05-11 / TASK-003 결과 기록

### 작업 브랜치

docs/rag-plan-by-codex

### 수행한 TASK

- TASK-003: 샘플 평가 질문 JSON 추가

### 수정한 파일

- docs/evaluation_questions.json
- docs/progress-log.md

### 완료한 작업

- 북브리프_돈의심리학.pdf 텍스트를 확인하고 평가 질문 근거로 사용할 문장을 선별
- MVP retrieval evaluation 용도에 맞춰 질문 6개 작성
- 각 질문에 expected_answer, expected_evidence, source_document, source_page, source_section, difficulty, question_type, metadata 포함

### 현재 상태

- 실제 검색 metric 계산은 TASK-013 범위이므로 구현하지 않았다.
- 샘플 질문은 현재 PDF의 1~2쪽에서 확인한 근거만 사용했다.
- TASK-003 변경사항은 아직 커밋하지 않았다.

### 다음에 할 일

- docs/evaluation_questions.json JSON 문법 검증
- TASK-002의 load_evaluation_questions로 샘플 질문 로드 검증
- TASK-003 변경 범위 검토
- TASK-003 커밋
- TASK-004 진행 전 별도 계획 작성

### 주의해야 할 점

- source_page는 PDF 추출 기준 페이지 번호를 수동으로 기록했다.
- expected_evidence는 검색 평가에 사용할 최소 근거 문장으로 작성했으며, 자동 채점 로직은 아직 없다.
- TASK-004 이후 청킹 전략 구현은 이번 작업 범위가 아니다.
