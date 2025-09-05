# FanTale

FanTale은 아이돌을 주제로 한 팬픽션(웹소설) 플랫폼입니다. 사용자의 선호(아이돌, 장르 등)를 분석해 개인화된 스토리를 LLM이 생성하며, 스토리는 장(챕터) 단위로 매일 일정 수량이 공개됩니다. 프리미엄 구독자는 더 많은 챕터를 열람할 수 있습니다.

## 기술 스택

- Backend
  - Python, FastAPI, Uvicorn
  - Celery + Redis (비동기 작업 / 오케스트레이션)
  - SQLAlchemy + SQLite(개발) — 다른 RDB로 대체 가능
  - Pydantic(BaseSettings) 기반 설정
  - LangChain / LangGraph 기반 스토리·챕터 에이전트 워크플로우
  - uv(패키지/가상환경), Ruff(포맷/린트)
- Frontend
  - Next.js 14 (React 18, TypeScript)
  - Tailwind CSS, lucide-react
  - TanStack Query
  - Turborepo 모노레포, pnpm(workspace)

## 실행 방법 (요약)

프로젝트 루트의 Makefile이 백엔드/프론트엔드 실행을 프록시합니다.

- 전체 개발 환경 동시 실행
  - 의존성 설치: `make install`
  - 동시 실행: `make dev`
  - 종료: `make stop`

- Backend만
  - 설치: `make install-backend`
  - 개발 서버(자동 리로드): `make dev-backend PORT=8000`
  - 일반 실행: `make run-backend PORT=8000`
  - Celery 워커/스케줄러/모니터: `make worker` · `make beat` · `make flower`
  - 기본 주소: http://127.0.0.1:8000 (OpenAPI: `/docs`)

- Frontend만
  - 설치: `make install-frontend`
  - 개발 서버: `make dev-frontend PORT=3000`
  - 프로덕션 모드(빌드 후 시작): `make dev-frontend-prod`
  - 기본 주소: http://localhost:3000

### 요구 사항
- Backend: Python, uv 설치(https://docs.astral.sh/uv/)
- Frontend: Node.js, pnpm 설치

## 동작 개요 (간략)
- 사용자가 선호를 설정하고 스토리 생성을 요청하면 FastAPI가 이를 수신하여 Celery 체인을 통해
  1) 스토리라인/플롯 생성 → 2) 챕터를 순차 생성·저장합니다.
- SQLAlchemy로 스토리/챕터를 DB에 저장하며, 클라이언트는 REST API로 상태와 결과를 조회합니다.
- 프론트엔드는 Next.js 앱이 API를 호출해 사용자별 스토리/챕터를 표시합니다.