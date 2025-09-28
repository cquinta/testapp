"""Rotas de healthcheck."""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..models import HealthResponse
from ..config import HEALTHTIME_THRESHOLD_SECONDS

router = APIRouter(tags=["Health"])

# Tempo de início da aplicação para o endpoint healthtime
start_time = datetime.now()

@router.get(
    "/healthcheck",
    response_model=HealthResponse,
    summary="Healthcheck básico",
    description="Endpoint de healthcheck que sempre retorna status saudável (200)",
    response_description="Status de saúde da aplicação"
)
def healthcheck() -> JSONResponse:
    """Endpoint básico de healthcheck que sempre retorna sucesso."""
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@router.get(
    "/healthcheck/error",
    summary="Healthcheck com erro",
    description="Endpoint que sempre retorna erro 500 para simular falhas",
    response_description="Status de erro da aplicação"
)
def error() -> JSONResponse:
    """Endpoint que simula uma falha retornando sempre erro 500."""
    return JSONResponse(content={"status": "error"}, status_code=500)

@router.get(
    "/healthtime",
    summary="Healthcheck baseado em tempo",
    description=f"Endpoint que retorna sucesso nos primeiros {HEALTHTIME_THRESHOLD_SECONDS} segundos após o start da aplicação, depois retorna erro 500",
    response_description="Status baseado no tempo de execução da aplicação"
)
def healthtime() -> dict:
    """Endpoint que simula degradação da aplicação ao longo do tempo.
    
    Comportamento:
    - Primeiros 60 segundos: Retorna status 'healthy'
    - Após 60 segundos: Retorna erro 500 'Erro no Servidor'
    """
    elapsed_time = datetime.now() - start_time
    if elapsed_time < timedelta(seconds=HEALTHTIME_THRESHOLD_SECONDS):
        return {"status": "healthy"}
    else:
        raise HTTPException(status_code=500, detail="Erro no Servidor")