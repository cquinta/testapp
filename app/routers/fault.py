"""Rotas de fault injection."""
import random
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..models import Healthcheck
from ..config import FAULT_NORMAL_OPTIONS, FAULT_SOFT_WEIGHTS

router = APIRouter(tags=["Fault Injection"])

@router.get(
    "/healthcheck/fault",
    response_model=Healthcheck,
    summary="Fault injection aleatório",
    description="Endpoint que retorna aleatoriamente status 200 (sucesso) ou 503 (indisponível) com 50% de chance cada",
    response_description="Status aleatório para simulação de falhas"
)
def fault() -> JSONResponse:
    """Endpoint de fault injection que retorna aleatoriamente sucesso ou falha.
    
    Retorna:
    - 200: Aplicação saudável (50% chance)
    - 503: Serviço indisponível (50% chance)
    """
    # Seleciona um status aleatoriamente
    random_status = random.choice(FAULT_NORMAL_OPTIONS)
    
    # Monta o corpo da resposta
    response_body = {
        "status": random_status,
        "description": "fault injection"
    }
    
    # Retorna uma resposta JSON com o status code e o corpo definidos dinamicamente
    return JSONResponse(status_code=random_status, content=response_body)

@router.get(
    "/healthcheck/fault/soft",
    response_model=Healthcheck,
    summary="Fault injection suave",
    description="Endpoint que retorna majoritariamente status 200 (87.5% chance) e ocasionalmente 503 (12.5% chance)",
    response_description="Status com baixa probabilidade de falha"
)
def soft() -> JSONResponse:
    """Endpoint de fault injection suave com baixa probabilidade de falha.
    
    Retorna:
    - 200: Aplicação saudável (87.5% chance - 7 em 8)
    - 503: Serviço indisponível (12.5% chance - 1 em 8)
    """
    # Seleciona um status aleatoriamente com pesos
    random_status = random.choice(FAULT_SOFT_WEIGHTS)
    
    # Monta o corpo da resposta
    response_body = {
        "status": random_status,
        "description": "fault injection"
    }
    
    # Retorna uma resposta JSON com o status code e o corpo definidos dinamicamente
    return JSONResponse(status_code=random_status, content=response_body)