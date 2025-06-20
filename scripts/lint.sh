#!/bin/bash
set -e

poetry run mypy --ignore-missing-imports .
poetry run isort --check --diff . tests/
poetry run black --check . tests/
poetry run flake8 . tests/

# Security check
poetry run bandit -r .
