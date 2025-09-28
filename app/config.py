"""Configurações da aplicação."""
import os

# Configurações da aplicação
APP_TITLE = "Test Application API"
APP_DESCRIPTION = "API para testes de healthcheck e fault injection com diferentes cenários de resposta"
APP_VERSION = "1.0.0"

# Configurações de tempo
HEALTHTIME_THRESHOLD_SECONDS = 60

# Configurações de fault injection
FAULT_SOFT_WEIGHTS = [200, 200, 200, 200, 200, 200, 200, 503]  # 87.5% success, 12.5% failure
FAULT_NORMAL_OPTIONS = [200, 503]  # 50% each

# Limites de performance
MAX_DURATION_SECONDS = 300  # 5 minutos máximo

# Variáveis de ambiente
def get_version() -> str:
    """Retorna a versão da aplicação da variável de ambiente."""
    return os.getenv("VERSION", "unknown")

def get_port() -> int:
    """Retorna a porta da aplicação."""
    return int(os.getenv("PORT", "8000"))

def get_host() -> str:
    """Retorna o host da aplicação."""
    return os.getenv("HOST", "0.0.0.0")

def get_sqs_queue_url() -> str:
    """Retorna a URL da fila SQS."""
    queue_url = os.getenv("SQS_QUEUE_URL")
    if not queue_url:
        raise ValueError("Variável de ambiente 'SQS_QUEUE_URL' não encontrada")
    return queue_url

