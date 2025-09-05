# FanTale Backend (FastAPI)

Dependency management: uv

## Prerequisites
- Python 3.11+
- uv installed: https://docs.astral.sh/uv/
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Setup
```bash
# from backend/ directory
uv venv
uv sync
```

## Run (dev)
You can run directly or use the Makefile targets:

```bash
# from backend/
# direct
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# or via Makefile
make dev            # reload on changes (defaults to port 8000)
make run            # run once

# Choose a different port
make dev PORT=8001
```

Open docs: http://127.0.0.1:8000/docs

## Notes
- Backend code lives under `app/` (no more src/ layout). The FastAPI app module is `app.main`.
- `pyproject.toml` is the single source of truth for dependencies. `requirements.txt` is not used.
- SQLite database file `fantale.db` will be created in the `backend/` directory on first run.
- Story persistence now uses SQLAlchemy repository under `app/db/repository.py`.
