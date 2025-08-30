import socket
import time
import random
import multiprocessing
import os
import psutil
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, Response
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel

app = FastAPI(
    title="Test Application API",
    description="API para testes de healthcheck e fault injection com diferentes cenários de resposta",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

def worker(quit_event: multiprocessing.Event):
    """
    Esta é a função que será executada em cada processo filho.
    Ela entra em um loop infinito ('busy-wait') que consome 100% de um núcleo da CPU.
    O loop continua até que o 'quit_event' seja sinalizado pelo processo principal.
    """
    while not quit_event.is_set():
        # A instrução 'pass' aqui cria um loop apertado que consome CPU.
        pass

start_time = datetime.now()

class Healthcheck(BaseModel):
    status: int
    description: str


@app.get(
    "/",
    tags=["Info"],
    summary="Obter hostname",
    description="Retorna o hostname do servidor onde a aplicação está executando",
    response_description="Hostname do servidor"
)
def read_root():
    """Endpoint raiz que retorna informações básicas do servidor."""
    hostname = socket.gethostname()
    return {"hostname": hostname}


@app.get(
    "/healthcheck",
    tags=["Health"],
    summary="Healthcheck básico",
    description="Endpoint de healthcheck que sempre retorna status saudável (200)",
    response_description="Status de saúde da aplicação"
)
def healthcheck():
    """Endpoint básico de healthcheck que sempre retorna sucesso."""
    return JSONResponse(content={"status": "healthy"}, status_code=200)


@app.get(
    "/healthcheck/error",
    tags=["Health"],
    summary="Healthcheck com erro",
    description="Endpoint que sempre retorna erro 500 para simular falhas",
    response_description="Status de erro da aplicação"
)
def error():
    """Endpoint que simula uma falha retornando sempre erro 500."""
    return JSONResponse(content={"status": "error"}, status_code=500)




@app.get(
    "/healthcheck/fault",
    response_model=Healthcheck,
    tags=["Fault Injection"],
    summary="Fault injection aleatório",
    description="Endpoint que retorna aleatoriamente status 200 (sucesso) ou 503 (indisponível) com 50% de chance cada",
    response_description="Status aleatório para simulação de falhas"
)
def fault():
    """Endpoint de fault injection que retorna aleatoriamente sucesso ou falha.
    
    Retorna:
    - 200: Aplicação saudável (50% chance)
    - 503: Serviço indisponível (50% chance)
    """
    # Lista de possíveis status HTTP
    possible_statuses: List[int] = [200, 503]

    # Seleciona um status aleatoriamente
    random_status: int = random.choice(possible_statuses)

    # Monta o corpo da resposta
    response_body = {
        "status": random_status,
        "description": "fault injection"
    }

    # Retorna uma resposta JSON com o status code e o corpo definidos dinamicamente
    return JSONResponse(status_code=random_status, content=response_body)

@app.get(
    "/healthcheck/fault/soft",
    response_model=Healthcheck,
    tags=["Fault Injection"],
    summary="Fault injection suave",
    description="Endpoint que retorna majoritariamente status 200 (87.5% chance) e ocasionalmente 503 (12.5% chance)",
    response_description="Status com baixa probabilidade de falha"
)
def soft():
    """Endpoint de fault injection suave com baixa probabilidade de falha.
    
    Retorna:
    - 200: Aplicação saudável (87.5% chance - 7 em 8)
    - 503: Serviço indisponível (12.5% chance - 1 em 8)
    """
    # Lista de possíveis status HTTP
    possible_statuses: List[int] = [200,200,200,200,200,200,200,503]

    # Seleciona um status aleatoriamente
    random_status: int = random.choice(possible_statuses)

    # Monta o corpo da resposta
    response_body = {
        "status": random_status,
        "description": "fault injection"
    }

    # Retorna uma resposta JSON com o status code e o corpo definidos dinamicamente
    return JSONResponse(status_code=random_status, content=response_body)


@app.get(
    "/healthtime",
    tags=["Health"],
    summary="Healthcheck baseado em tempo",
    description="Endpoint que retorna sucesso nos primeiros 60 segundos após o start da aplicação, depois retorna erro 500",
    response_description="Status baseado no tempo de execução da aplicação"
)
def healthtime():
    """Endpoint que simula degradação da aplicação ao longo do tempo.
    
    Comportamento:
    - Primeiros 60 segundos: Retorna status 'healthy'
    - Após 60 segundos: Retorna erro 500 'Erro no Servidor'
    """
    elapsed_time = datetime.now() - start_time
    if elapsed_time < timedelta(seconds=60):
        return {"status": "healthy"}
    else:
        raise HTTPException(status_code=500, detail="Erro no Servidor")

def get_memory_usage_mb():
    """Retorna o uso de memória atual do processo em MB.
    
    Returns:
        float: Uso de memória em megabytes
    """
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)
    
@app.get(
    "/cpu/{duration_seconds}",
    tags=["Performance"],
    summary="Stress test de CPU",
    description="Endpoint que executa stress test em todos os núcleos da CPU pelo tempo especificado em segundos",
    response_description="Status do teste de stress da CPU"
)
async def cpu_on_fire(duration_seconds: int):
    """Endpoint que executa stress test intensivo da CPU.
    
    Args:
        duration_seconds: Duração em segundos para executar o stress test
    
    Comportamento:
    - Cria um processo worker para cada núcleo da CPU disponível
    - Cada processo executa um loop infinito consumindo 100% do núcleo
    - Executa pelo tempo especificado no parâmetro duration_seconds
    - Finaliza todos os processos e retorna status 'On Fire'
    
    Atenção: Este endpoint pode causar alta utilização de CPU no servidor!
    """
    # 1. Obter o número de núcleos de CPU disponíveis no sistema.
    # Equivalente a `runtime.NumCPU()` em Go.
    cpu_cores = os.cpu_count()
    if cpu_cores is None:
        return JSONResponse(status_code=500, content={"error": "Não foi possível determinar o número de núcleos da CPU."})

    print(f"Iniciando stress test em {cpu_cores} núcleo(s) da CPU...")

    # 2. Criar um objeto de Evento.
    # Este evento será usado para sinalizar aos processos 'worker' que eles devem parar.
    # É o equivalente ao `chan bool` em Go.
    quit_event = multiprocessing.Event()

    processes = []
    # 3. Iniciar um processo 'worker' para cada núcleo da CPU.
    # Equivalente ao loop `go func() {}` em Go.
    for i in range(cpu_cores):
        process = multiprocessing.Process(target=worker, args=(quit_event,))
        processes.append(process)
        process.start()
        print(f"Processo worker {i+1} iniciado no PID {process.pid}")

    # 4. Esperar por 3 segundos enquanto os processos 'worker' consomem a CPU.
    # Equivalente a `time.Sleep(3 * time.Second)` em Go.
    time.sleep(duration_seconds)

    # 5. Sinalizar para todos os processos pararem.
    # Define o evento, o que fará com que a condição `while` nos workers se torne falsa.
    # Equivalente a enviar para o canal `quit <- true`.
    print("Enviando sinal para parar os processos workers...")
    quit_event.set()

    # 6. Esperar que todos os processos terminem.
    # Isso garante que a função só retorne depois que os workers forem encerrados.
    for process in processes:
        process.join()

    print("Stress test concluído.")

    # 7. Retornar a resposta JSON.
    # Equivalente a `c.JSON(http.StatusOK, gin.H{"status": "On Fire"})`.
    return {"status": "On Fire"}

@app.get(
    "/version",
    tags=["Info"],
    summary="Obter versão",
    description="Retorna a versão da aplicação através da variável de ambiente VERSION",
    response_description="Versão da aplicação ou erro se não definida"
)
def get_version():
    """Endpoint que retorna a versão da aplicação.
    
    Retorna:
    - 200: Versão da aplicação se a variável VERSION estiver definida
    - 404: Erro se a variável de ambiente VERSION não estiver definida
    """
    version = os.getenv("VERSION")
    if version is None:
        return Response(content="Variável de ambiente 'VERSION' não encontrada.", status_code=status.HTTP_404_NOT_FOUND)
    return {"version": version}

@app.get(
    "/mem/{duration_seconds}",
    tags=["Performance"],
    summary="Stress test de memória",
    description="Endpoint que consome CPU e memória intensivamente pelo tempo especificado em segundos",
    response_description="Status do teste de stress de memória com métricas detalhadas"
)
async def mem(duration_seconds: int):
    """Endpoint que executa stress test intensivo de CPU e memória.
    
    Args:
        duration_seconds: Duração em segundos para executar o stress test
    
    Comportamento:
    - Monitora uso de memória antes e depois do teste
    - Cria uma lista crescente para consumir memória
    - Executa loop intensivo para consumir CPU
    - Retorna métricas detalhadas do consumo de recursos
    
    Atenção: Este endpoint pode causar alta utilização de CPU e memória!
    """
    mem_before = get_memory_usage_mb()
    print(f"Iniciando operação de consumo de recursos por {duration_seconds} segundo(s)...")
    print(f"Uso de memória antes: {mem_before:.2f} MB")

    start_time = time.monotonic()
    s = []
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

    return {
        "status": "On Fire",
        "message": "Operação de consumo de recursos concluída.",
        "requested_duration_seconds": duration_seconds,
        "actual_duration_seconds": round(actual_duration, 4),
        "items_created_in_list": len(s),
        "memory_allocated_mb": round(mem_after - mem_before, 2)
    }