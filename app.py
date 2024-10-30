from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import socket

app = FastAPI()

start_time = datetime.now()

@app.get("/")
def read_root():
    hostname = socket.gethostname()
    return {"hostname": hostname}

@app.get("/health")
def health():
    
    return {"status": "healthy"}

@app.get("/healthtime")
def healthtime():
    elapsed_time = datetime.now() - start_time
    if elapsed_time < timedelta(seconds=60):
        return {"status": "healthy"}
    else:
        raise HTTPException(status_code=500, detail="Erro no Servidor")

