#!/bin/bash
set -e

poetry run isort . tests/
poetry run black . tests/
