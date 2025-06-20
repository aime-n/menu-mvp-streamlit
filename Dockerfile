# Usar a mesma versão do Python que o CI/CD
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry

# Copiar arquivos de configuração
COPY pyproject.toml poetry.lock ./

# Configurar Poetry para não criar ambiente virtual (já estamos no container)
RUN poetry config virtualenvs.create false

# Instalar dependências 
RUN poetry install --with dev

# Copiar código do projeto
COPY . .

# Comando padrão para rodar os testes
CMD ["poetry", "run", "pytest", "tests/", "-v"] 