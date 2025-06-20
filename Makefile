.PHONY: help clean test install dev-install lint format check docker-test done docker-app docker-shell docker-lint docker-format

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Clean and format code
	./scripts/clean.sh

test: ## Run tests
	./scripts/test.sh

install: ## Install dependencies
	poetry install

dev-install: ## Install development dependencies
	poetry install --with dev

lint: ## Run linting checks
	poetry run flake8 . tests/
	poetry run mypy .

format: ## Format code
	poetry run isort . tests/
	poetry run black . tests/

check: ## Run all checks (lint, format, test)
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) test

run: ## Run Streamlit app
	poetry run streamlit run app.py

docker-test: ## Test in Docker (simulates CI/CD environment)
	./scripts/docker-test.sh

docker-app: ## Run Streamlit app in Docker
	docker-compose up app

docker-shell: ## Open shell in Docker container
	docker-compose run --rm shell

docker-lint: ## Run linting in Docker
	docker-compose run --rm lint

docker-format: ## Run formatting in Docker
	docker-compose run --rm format

done: ## Clean, update lockfile and test
	./scripts/done.sh
