"""Aplicação principal FastAPI."""
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .config import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from .routers import info, health, fault, performance, messaging

def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI."""
    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Incluir routers
    app.include_router(info.router)
    app.include_router(health.router)
    app.include_router(fault.router)
    app.include_router(performance.router)
    app.include_router(messaging.router)
    
    # Configurar métricas Prometheus
    Instrumentator().instrument(app).expose(app)
    
    return app

# Instância da aplicação
app = create_app()