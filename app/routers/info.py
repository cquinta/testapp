"""Rotas de informações do sistema."""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from ..models import HostnameResponse, VersionResponse
from ..services.system_service import get_hostname, get_version_from_env

router = APIRouter(tags=["Info"])

@router.get(
    "/",
    response_model=HostnameResponse,
    summary="Obter hostname",
    description="Retorna o hostname do servidor onde a aplicação está executando",
    response_description="Hostname do servidor"
)
def read_root() -> HostnameResponse:
    """Endpoint raiz que retorna informações básicas do servidor."""
    hostname = get_hostname()
    return HostnameResponse(hostname=hostname)

@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Obter versão",
    description="Retorna a versão da aplicação através da variável de ambiente VERSION",
    response_description="Versão da aplicação ou erro se não definida"
)
def get_version() -> VersionResponse:
    """Endpoint que retorna a versão da aplicação.
    
    Returns:
        VersionResponse: Versão da aplicação se a variável VERSION estiver definida
        
    Raises:
        HTTPException: 404 se a variável de ambiente VERSION não estiver definida
    """
    try:
        version = get_version_from_env()
        return VersionResponse(version=version)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )