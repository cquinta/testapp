"""Ponto de entrada principal para manter compatibilidade."""
from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.config import get_host, get_port
    
    uvicorn.run(app, host=get_host(), port=get_port())