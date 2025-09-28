"""Serviços relacionados ao stress test de CPU."""
import time
import multiprocessing
from typing import List

def worker(quit_event: multiprocessing.Event) -> None:
    """Worker que consome 100% de um núcleo da CPU.
    
    Esta função será executada em cada processo filho.
    Ela entra em um loop infinito ('busy-wait') que consome 100% de um núcleo da CPU.
    O loop continua até que o 'quit_event' seja sinalizado pelo processo principal.
    
    Args:
        quit_event: Evento para sinalizar quando parar o worker
    """
    while not quit_event.is_set():
        # A instrução 'pass' aqui cria um loop apertado que consome CPU
        pass

def run_cpu_stress_test(duration_seconds: int, cpu_cores: int) -> None:
    """Executa stress test de CPU por um tempo determinado.
    
    Args:
        duration_seconds: Duração do teste em segundos
        cpu_cores: Número de núcleos de CPU para usar
    """
    print(f"Iniciando stress test em {cpu_cores} núcleo(s) da CPU...")
    
    # Criar evento para controlar os workers
    quit_event = multiprocessing.Event()
    processes: List[multiprocessing.Process] = []
    
    try:
        # Iniciar um processo worker para cada núcleo da CPU
        for i in range(cpu_cores):
            process = multiprocessing.Process(target=worker, args=(quit_event,))
            processes.append(process)
            process.start()
            print(f"Processo worker {i+1} iniciado no PID {process.pid}")
        
        # Esperar pela duração especificada
        time.sleep(duration_seconds)
        
    finally:
        # Sinalizar para todos os processos pararem
        print("Enviando sinal para parar os processos workers...")
        quit_event.set()
        
        # Esperar que todos os processos terminem
        for process in processes:
            process.join()
        
        print("Stress test concluído.")

