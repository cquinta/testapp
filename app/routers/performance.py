"""Rotas de performance e stress testing."""
from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import JSONResponse

from ..models import CPUStressResponse, MemoryStressResponse
from ..services.cpu_service import run_cpu_stress_test
from ..services.memory_service import run_memory_stress_test
from ..services.system_service import get_cpu_count
from ..config import MAX_DURATION_SECONDS

router = APIRouter(tags=["Performance"])

@router.get(
    "/cpu/{duration_seconds}",
    response_model=CPUStressResponse,
    summary="Stress test de CPU",
    description="Endpoint que executa stress test em todos os núcleos da CPU pelo tempo especificado em segundos",
    response_description="Status do teste de stress da CPU"
)
async def cpu_on_fire(
    duration_seconds: int = Path(..., ge=1, le=MAX_DURATION_SECONDS, description="Duração em segundos (1-300)")
) -> CPUStressResponse:
    """Endpoint que executa stress test intensivo da CPU.
    
    Args:
        duration_seconds: Duração em segundos para executar o stress test (1-300)
    
    Comportamento:
    - Cria um processo worker para cada núcleo da CPU disponível
    - Cada processo executa um loop infinito consumindo 100% do núcleo
    - Executa pelo tempo especificado no parâmetro duration_seconds
    - Finaliza todos os processos e retorna status 'On Fire'
    
    Atenção: Este endpoint pode causar alta utilização de CPU no servidor!
    """
    try:
        cpu_cores = get_cpu_count()
        run_cpu_stress_test(duration_seconds, cpu_cores)
        return CPUStressResponse(status="On Fire")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/mem/{duration_seconds}",
    response_model=MemoryStressResponse,
    summary="Stress test de memória",
    description="Endpoint que consome CPU e memória intensivamente pelo tempo especificado em segundos",
    response_description="Status do teste de stress de memória com métricas detalhadas"
)
async def mem(
    duration_seconds: int = Path(..., ge=1, le=MAX_DURATION_SECONDS, description="Duração em segundos (1-300)")
) -> MemoryStressResponse:
    """Endpoint que executa stress test intensivo de CPU e memória.
    
    Args:
        duration_seconds: Duração em segundos para executar o stress test (1-300)
    
    Comportamento:
    - Monitora uso de memória antes e depois do teste
    - Cria uma lista crescente para consumir memória
    - Executa loop intensivo para consumir CPU
    - Retorna métricas detalhadas do consumo de recursos
    
    Atenção: Este endpoint pode causar alta utilização de CPU e memória!
    """
    actual_duration, items_created, memory_allocated = run_memory_stress_test(duration_seconds)
    
    return MemoryStressResponse(
        status="On Fire",
        message="Operação de consumo de recursos concluída.",
        requested_duration_seconds=duration_seconds,
        actual_duration_seconds=round(actual_duration, 4),
        items_created_in_list=items_created,
        memory_allocated_mb=round(memory_allocated, 2)
    )