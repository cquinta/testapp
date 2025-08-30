# =============================================================================
# Test Application API - Dockerfile
# =============================================================================
# Este Dockerfile cria uma imagem Docker para a Test Application API,
# uma aplicação FastAPI para testes de healthcheck e fault injection.
# 
# Utiliza multi-stage build para otimizar o tamanho da imagem final:
# - Stage 1 (dev): Instala dependências em um ambiente virtual
# - Stage 2 (production): Copia apenas os arquivos necessários
# =============================================================================

# -----------------------------------------------------------------------------
# STAGE 1: Development - Instalação de dependências
# -----------------------------------------------------------------------------
# Usa imagem Chainguard Python com ferramentas de desenvolvimento
FROM cgr.dev/chainguard/python:latest-dev AS dev

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Configura o PATH para incluir o ambiente virtual
ENV PATH="/app/venv/bin:$PATH"

# Cria ambiente virtual Python para isolar dependências
RUN python -m venv venv

# Copia arquivo de dependências
COPY requirements.txt requirements.txt

# Instala dependências Python no ambiente virtual
# --no-cache-dir: Não armazena cache para reduzir tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# STAGE 2: Production - Imagem final otimizada
# -----------------------------------------------------------------------------
# Usa imagem Chainguard Python mais leve (sem ferramentas de desenvolvimento)
FROM cgr.dev/chainguard/python:latest

# Define o diretório de trabalho
WORKDIR /app

# Configura o PATH para usar o ambiente virtual
ENV PATH="/app/venv/bin:$PATH"

# Copia o código da aplicação
COPY app.py app.py

# Copia o ambiente virtual com dependências instaladas do stage anterior
COPY --from=dev /app/venv /app/venv

# Expõe a porta 8000 para acesso externo
EXPOSE 8000

# Define o comando de inicialização da aplicação
# uvicorn: Servidor ASGI para FastAPI
# app:app: Módulo 'app' e instância 'app' do FastAPI
# --host 0.0.0.0: Aceita conexões de qualquer IP
# --port 8000: Porta de escuta
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
