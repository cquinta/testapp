from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import socket
import random
from typing import List
from pydantic import BaseModel

app = FastAPI(
    title="Test Application API",
    description="API para testes de healthcheck e fault injection com diferentes cenários de resposta",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

start_time = datetime.now()

class Healthcheck(BaseModel):
    status: int
    description: str


@app.get(
    "/",
    tags=["Info"],
    summary="Obter hostname",
    description="Retorna o hostname do servidor onde a aplicação está executando",
    response_description="Hostname do servidor"
)
def read_root():
    """Endpoint raiz que retorna informações básicas do servidor."""
    hostname = socket.gethostname()
    return {"hostname": hostname}


@app.get(
    "/healthcheck",
    tags=["Health"],
    summary="Healthcheck básico",
    description="Endpoint de healthcheck que sempre retorna status saudável (200)",
    response_description="Status de saúde da aplicação"
)
def healthcheck():
    """Endpoint básico de healthcheck que sempre retorna sucesso."""
    return JSONResponse(content={"status": "healthy"}, status_code=200)


@app.get(
    "/healthcheck/error",
    tags=["Health"],
    summary="Healthcheck com erro",
    description="Endpoint que sempre retorna erro 500 para simular falhas",
    response_description="Status de erro da aplicação"
)
def error():
    """Endpoint que simula uma falha retornando sempre erro 500."""
    return JSONResponse(content={"status": "error"}, status_code=500)




@app.get(
    "/healthcheck/fault",
    response_model=Healthcheck,
    tags=["Fault Injection"],
    summary="Fault injection aleatório",
    description="Endpoint que retorna aleatoriamente status 200 (sucesso) ou 503 (indisponível) com 50% de chance cada",
    response_description="Status aleatório para simulação de falhas"
)
def fault():
    """Endpoint de fault injection que retorna aleatoriamente sucesso ou falha.
    
    Retorna:
    - 200: Aplicação saudável (50% chance)
    - 503: Serviço indisponível (50% chance)
    """
    # Lista de possíveis status HTTP
    possible_statuses: List[int] = [200, 503]

    # Seleciona um status aleatoriamente
    random_status: int = random.choice(possible_statuses)

    # Monta o corpo da resposta
    response_body = {
        "status": random_status,
        "description": "fault injection"
    }

    # Retorna uma resposta JSON com o status code e o corpo definidos dinamicamente
    return JSONResponse(status_code=random_status, content=response_body)

@app.get(
    "/healthcheck/fault/soft",
    response_model=Healthcheck,
    tags=["Fault Injection"],
    summary="Fault injection suave",
    description="Endpoint que retorna majoritariamente status 200 (87.5% chance) e ocasionalmente 503 (12.5% chance)",
    response_description="Status com baixa probabilidade de falha"
)
def soft():
    """Endpoint de fault injection suave com baixa probabilidade de falha.
    
    Retorna:
    - 200: Aplicação saudável (87.5% chance - 7 em 8)
    - 503: Serviço indisponível (12.5% chance - 1 em 8)
    """
    # Lista de possíveis status HTTP
    possible_statuses: List[int] = [200,200,200,200,200,200,200,503]

    # Seleciona um status aleatoriamente
    random_status: int = random.choice(possible_statuses)

    # Monta o corpo da resposta
    response_body = {
        "status": random_status,
        "description": "fault injection"
    }

    # Retorna uma resposta JSON com o status code e o corpo definidos dinamicamente
    return JSONResponse(status_code=random_status, content=response_body)


@app.get(
    "/healthtime",
    tags=["Health"],
    summary="Healthcheck baseado em tempo",
    description="Endpoint que retorna sucesso nos primeiros 60 segundos após o start da aplicação, depois retorna erro 500",
    response_description="Status baseado no tempo de execução da aplicação"
)
def healthtime():
    """Endpoint que simula degradação da aplicação ao longo do tempo.
    
    Comportamento:
    - Primeiros 60 segundos: Retorna status 'healthy'
    - Após 60 segundos: Retorna erro 500 'Erro no Servidor'
    """
    elapsed_time = datetime.now() - start_time
    if elapsed_time < timedelta(seconds=60):
        return {"status": "healthy"}
    else:
        raise HTTPException(status_code=500, detail="Erro no Servidor")
