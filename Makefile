.PHONY: dev test lint format build clean help

# Development
dev:
	@echo "Starting development servers..."
	@cd backend && pip install -e ".[dev]" && uvicorn api.main:app --reload --port 8000 &
	@cd frontend && npm install && npm run dev &
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"

dev-backend:
	@cd backend && pip install -e ".[dev]" && uvicorn api.main:app --reload --port 8000

dev-frontend:
	@cd frontend && npm install && npm run dev

# Testing
test:
	@echo "Running all tests..."
	@cd backend && pytest -v --cov=az_sim --cov=api
	@cd frontend && npm run test

test-backend:
	@cd backend && pytest -v --cov=az_sim --cov=api

test-frontend:
	@cd frontend && npm run test

# Linting
lint:
	@echo "Running linters..."
	@cd backend && ruff check . && mypy .
	@cd frontend && npm run lint

lint-backend:
	@cd backend && ruff check . && mypy .

lint-frontend:
	@cd frontend && npm run lint

# Formatting
format:
	@echo "Formatting code..."
	@cd backend && ruff format .
	@cd frontend && npm run format

format-backend:
	@cd backend && ruff format .

format-frontend:
	@cd frontend && npm run format

# Docker
build:
	@docker compose build

up:
	@docker compose up

up-d:
	@docker compose up -d

down:
	@docker compose down

logs:
	@docker compose logs -f

# Clean
clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Help
help:
	@echo "Azerbaijan Simplified Tax Calculator - Development Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev            Start both backend and frontend in dev mode"
	@echo "  make dev-backend    Start only backend in dev mode"
	@echo "  make dev-frontend   Start only frontend in dev mode"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run all tests"
	@echo "  make test-backend   Run backend tests only"
	@echo "  make test-frontend  Run frontend tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run linters on all code"
	@echo "  make format         Format all code"
	@echo ""
	@echo "Docker:"
	@echo "  make build          Build Docker images"
	@echo "  make up             Start Docker containers"
	@echo "  make up-d           Start Docker containers (detached)"
	@echo "  make down           Stop Docker containers"
	@echo "  make logs           View Docker logs"
	@echo ""
	@echo "Other:"
	@echo "  make clean          Clean up temporary files"
	@echo "  make help           Show this help message"
