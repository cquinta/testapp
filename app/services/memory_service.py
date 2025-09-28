"""Serviços relacionados ao stress test de memória."""
import time
from typing import Tuple, List
from .system_service import get_memory_usage_mb

def run_memory_stress_test(duration_seconds: int) -> Tuple[float, int, float]:
    """Executa stress test de memória e CPU por um tempo determinado.
    
    Args:
        duration_seconds: Duração do teste em segundos
        
    Returns:
        Tuple contendo:
        - actual_duration: Duração real do teste
        - items_created: Número de itens criados na lista
        - memory_allocated: Memória alocada em MB
    """
    mem_before = get_memory_usage_mb()
    print(f"Iniciando operação de consumo de recursos por {duration_seconds} segundo(s)...")
    print(f"Uso de memória antes: {mem_before:.2f} MB")
    
    start_time = time.monotonic()
    s: List[int] = []
    soma_atual = 0
    
    # Loop que executa e consome recursos pela duração especificada
    while (time.monotonic() - start_time) < duration_seconds:
        soma_atual += 1
        s.append(soma_atual)
        # Este loop mantém a CPU ocupada e a memória crescendo
    
    end_time = time.monotonic()
    actual_duration = end_time - start_time
    mem_after = get_memory_usage_mb()
    
    print(f"Operação concluída em {actual_duration:.2f} segundos.")
    print(f"Uso de memória depois: {mem_after:.2f} MB")
    
    return actual_duration, len(s), mem_after - mem_before