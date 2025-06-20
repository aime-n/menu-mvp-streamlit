#!/bin/bash
set -euxo pipefail

# Construir a imagem Docker
docker build -t menu-mvp-streamlit-test .

# Rodar os testes no container
docker run --rm menu-mvp-streamlit-test

echo "✅ Testes no Docker executados com sucesso!" 