"""Serviços relacionados ao sistema."""
import socket
import psutil
import os

def get_hostname() -> str:
    """Retorna o hostname do servidor."""
    return socket.gethostname()

def get_memory_usage_mb() -> float:
    """Retorna o uso de memória atual do processo em MB.
    
    Returns:
        float: Uso de memória em megabytes
    """
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def get_cpu_count() -> int:
    """Retorna o número de núcleos de CPU disponíveis."""
    cpu_cores = os.cpu_count()
    if cpu_cores is None:
        raise RuntimeError("Não foi possível determinar o número de núcleos da CPU")
    return cpu_cores

def get_version_from_env() -> str:
    """Retorna a versão da aplicação da variável de ambiente."""
    version = os.getenv("VERSION")
    if version is None:
        raise ValueError("Variável de ambiente 'VERSION' não encontrada")
    return version