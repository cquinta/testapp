# Utiliza uma imagem base do Python 3.9 slim
FROM  cgr.dev/chainguard/python:latest-dev AS dev  

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Instala as dependências

ENV PATH="/app/venv/bin:$PATH"
RUN python -m venv venv
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do aplicativo

FROM cgr.dev/chainguard/python:latest
WORKDIR /app
ENV PATH="/app/venv/bin:$PATH"
COPY app.py app.py
COPY --from=dev /app/venv /app/venv
# Expõe a porta que o aplicativo irá utilizar
EXPOSE 8000


# Comando para iniciar o aplicativo
ENTRYPOINT [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
