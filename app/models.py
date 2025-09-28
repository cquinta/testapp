"""Modelos Pydantic da aplicação."""
from pydantic import BaseModel, Field
from typing import Optional

class Healthcheck(BaseModel):
    """Modelo para resposta de healthcheck."""
    status: int = Field(..., description="Status HTTP retornado")
    description: str = Field(..., description="Descrição do status")

class HostnameResponse(BaseModel):
    """Modelo para resposta de hostname."""
    hostname: str = Field(..., description="Nome do host do servidor")

class VersionResponse(BaseModel):
    """Modelo para resposta de versão."""
    version: str = Field(..., description="Versão da aplicação")

class HealthResponse(BaseModel):
    """Modelo para resposta de health básico."""
    status: str = Field(..., description="Status de saúde da aplicação")

class CPUStressResponse(BaseModel):
    """Modelo para resposta de stress test de CPU."""
    status: str = Field(..., description="Status do teste")

class MemoryStressResponse(BaseModel):
    """Modelo para resposta de stress test de memória."""
    status: str = Field(..., description="Status do teste")
    message: str = Field(..., description="Mensagem descritiva")
    requested_duration_seconds: int = Field(..., description="Duração solicitada em segundos")
    actual_duration_seconds: float = Field(..., description="Duração real em segundos")
    items_created_in_list: int = Field(..., description="Número de itens criados na lista")
    memory_allocated_mb: float = Field(..., description="Memória alocada em MB")

class MessageRequest(BaseModel):
    """Modelo para requisição de envio de mensagem."""
    message: str = Field(..., description="Mensagem a ser enviada para a fila SQS")

class MessageResponse(BaseModel):
    """Modelo para resposta de envio de mensagem."""
    status: str = Field(..., description="Status do envio")
    message_id: str = Field(..., description="ID da mensagem na fila SQS")
    queue_url: str = Field(..., description="URL da fila SQS utilizada")

class ReceiveMessageResponse(BaseModel):
    """Modelo para resposta de recebimento de mensagem."""
    status: str = Field(..., description="Status da operação")
    message_id: Optional[str] = Field(None, description="ID da mensagem recebida")
    body: Optional[str] = Field(None, description="Conteúdo da mensagem")
    queue_url: str = Field(..., description="URL da fila SQS utilizada")
    message: str = Field(..., description="Mensagem descritiva do resultado")


