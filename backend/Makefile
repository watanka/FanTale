.PHONY: install dev run fmt lint worker beat flower

PORT ?= 8000

install:
	uv venv
	uv sync

run:
	uv run uvicorn app.main:app --host 127.0.0.1 --port $(PORT)

dev:
	uv run uvicorn app.main:app --reload --host 127.0.0.1 --port $(PORT)

fmt:
	uv run ruff format

lint:
	uv run ruff check

# --- Celery (Redis broker) ---
worker:
	uv run celery -A app.celery_app.celery worker -l info

beat:
	uv run celery -A app.celery_app.celery beat -l info

flower:
	uv run celery -A app.celery_app.celery flower
