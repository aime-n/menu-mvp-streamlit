#!/bin/bash
set -e

poetry run pytest -s --cov=. --cov=tests --cov-report=term-missing ${@-} --cov-report html
