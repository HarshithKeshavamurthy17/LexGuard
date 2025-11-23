.PHONY: setup api ui run lint format test clean help

help:
	@echo "LexGuard Contract AI - Makefile Commands"
	@echo "========================================"
	@echo "setup    : Install dependencies with Poetry"
	@echo "api      : Run FastAPI backend (port 8000)"
	@echo "ui       : Run Streamlit frontend (port 8501)"
	@echo "run      : Run both API and UI concurrently"
	@echo "lint     : Run ruff linter"
	@echo "format   : Format code with black"
	@echo "test     : Run pytest tests"
	@echo "clean    : Remove data, cache, and build files"

setup:
	poetry install

api:
	poetry run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

ui:
	poetry run streamlit run app/streamlit_app.py --server.port 8501

run:
	@echo "Starting LexGuard Contract AI..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:8501"
	@echo "Press Ctrl+C to stop both services"
	@(trap 'kill 0' SIGINT; \
		poetry run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 & \
		poetry run streamlit run app/streamlit_app.py --server.port 8501 & \
		wait)

lint:
	poetry run ruff check .

format:
	poetry run black .

test:
	poetry run pytest -v

clean:
	rm -rf data/ .pytest_cache/ .ruff_cache/ __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

