# AGENTS.md

## Working Rules

- 이전 대화 기록에 의존하지 말고, 항상 repository 문서와 Git 상태를 기준으로 작업한다.
- 작업 시작 전 다음 파일을 확인한다.
  - docs/project-plan.md
  - docs/tasks.md
  - docs/progress-log.md
- 한 번에 하나의 TASK만 수행한다.
- TASK 범위를 벗어난 변경은 하지 않는다.
- 파일 수정 전에는 먼저 계획을 제시한다.
- 사용자가 승인하기 전에는 파일을 수정하지 않는다.
- 작업 완료 후 docs/progress-log.md를 업데이트한다.

## Git Rules

- 작업 전 `git status`를 확인한다.
- 작업 전 현재 브랜치를 확인한다.
- 한 TASK는 하나의 커밋으로 관리한다.
- 커밋 메시지는 conventional commit 형식을 사용한다.
- 커밋 전 변경사항이 TASK 범위 안인지 확인한다.

## Verification Rules

- 가능한 경우 테스트 또는 실행 검증을 수행한다.
- 검증을 수행하지 못한 경우 이유를 명확히 기록한다.
- 실패한 테스트나 오류를 숨기지 않는다.

## Documentation Rules

- 프로젝트 계획은 docs/project-plan.md를 기준으로 한다.
- 작업 목록은 docs/tasks.md를 기준으로 한다.
- 진행 상태는 docs/progress-log.md에 기록한다.
