# Test Application API

Uma API FastAPI para testes de healthcheck, fault injection e stress testing de CPU e memória e mensageria.

> **Nota**: Esta é uma tentativa de criar uma versão em Python com funcionalidades inspiradas no aplicativo em Go "chip", encontrado em https://github.com/msfidelis/chip

## 📋 Visão Geral

Esta aplicação fornece endpoints para simular diferentes cenários de teste, incluindo:
- Healthchecks básicos e com falhas
- Fault injection com diferentes probabilidades
- Stress testing de CPU e memória
- Informações do servidor
- Envio de mensagens para filas SQS
- Leitura e deleção de mensagems para filas SQS

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.7+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd testapp
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
# Opção 1: Usando uvicorn diretamente
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Opção 2: Usando o script principal
python main.py
```

### Usando Docker

```bash
docker build -t moc-app .
docker run -p 8000:8000 moc-app
```

## 📖 Documentação da API

A documentação interativa está disponível em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Endpoints

### Info
- `GET /` - Retorna o hostname do servidor
- `GET /version` - Retorna a versão da aplicação (variável VERSION)

### Health
- `GET /healthcheck` - Healthcheck básico (sempre retorna 200)
- `GET /healthcheck/error` - Sempre retorna erro 500
- `GET /healthtime` - Retorna sucesso por 60s, depois erro 500

### Fault Injection
- `GET /healthcheck/fault` - Retorna aleatoriamente 200 ou 503 (50% cada)
- `GET /healthcheck/fault/soft` - Retorna 200 (87.5%) ou 503 (12.5%)

### Performance
- `GET /cpu/{duration_seconds}` - Executa stress test de CPU pelo tempo especificado
- `GET /mem/{duration_seconds}` - Executa stress test de memória e CPU pelo tempo especificado

### Messaging
- `POST /sent-message` - Envia mensagem para fila SQS

## 💡 Exemplos de Uso

### Healthcheck básico
```bash
curl http://localhost:8000/healthcheck
# Resposta: {"status": "healthy"}
```

### Fault injection
```bash
curl http://localhost:8000/healthcheck/fault
# Resposta: {"status": 200, "description": "fault injection"} ou
# Resposta: {"status": 503, "description": "fault injection"}
```

### Stress test de CPU
```bash
curl http://localhost:8000/cpu/5
# Executa stress test por 5 segundos
# Resposta: {"status": "On Fire"}
```

### Obter hostname
```bash
curl http://localhost:8000/
# Resposta: {"hostname": "nome-do-servidor"}
```

### Obter versão
```bash
export VERSION="1.0.0"
curl http://localhost:8000/version
# Resposta: {"version": "1.0.0"}
```

### Stress test de memória
```bash
curl http://localhost:8000/mem/3
# Executa stress test de memória por 3 segundos
# Resposta: {"status": "On Fire", "memory_allocated_mb": 45.2, ...}
```

### Enviar mensagem para SQS
```bash
export SQS_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue"
curl -X POST http://localhost:8000/sent-message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello SQS!"}'
# Resposta: {"status": "success", "message_id": "abc123", "queue_url": "..."}
```

## ⚠️ Avisos Importantes

- Os endpoints `/cpu/{duration_seconds}` e `/mem/{duration_seconds}` podem causar alta utilização de recursos
- O endpoint `/healthtime` muda comportamento após 60 segundos de execução
- O endpoint `/version` requer a variável de ambiente VERSION definida
- O endpoint `/sent-message` requer a variável de ambiente SQS_QUEUE_URL definida
- Use os endpoints de fault injection para simular falhas em testes

## 🛠️ Desenvolvimento

### Arquitetura

O projeto foi organizado da seguinte maneira:

- **Routers**: Endpoints organizados por categoria (info, health, fault, performance, messaging)
- **Services**: Lógica de negócio isolada 
- **Models**: Modelos Pydantic centralizados para validação
- **Config**: Configurações e constantes em arquivo dedicado


### Estrutura do Projeto
```
testapp/
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicação principal FastAPI
│   ├── config.py        # Configurações e constantes
│   ├── models.py        # Modelos Pydantic
│   ├── routers/         # Endpoints organizados por categoria
│   │   ├── __init__.py
│   │   ├── info.py         # Endpoints de informações
│   │   ├── health.py       # Endpoints de health
│   │   ├── fault.py        # Endpoints de fault injection
│   │   ├── performance.py  # Endpoints de performance
│   │   └── messaging.py    # Endpoints de mensageria
│   └── services/        # Lógica de negócio
│       ├── __init__.py
│       ├── system_service.py    # Serviços do sistema
│       ├── cpu_service.py       # Stress test de CPU
│       ├── memory_service.py    # Stress test de memória
│       └── sqs_service.py       # Serviços de SQS
├── main.py             # Ponto de entrada
├── requirements.txt    # Dependências Python
├── Dockerfile         # Configuração Docker
└── README.md          # Este arquivo
```

### Dependências
- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validação de dados
- **psutil**: Monitoramento de recursos do sistema
- **boto3**: SDK da AWS para integração com SQS

## 📊 Monitoramento

Para monitorar a aplicação, você pode usar os endpoints de healthcheck:

```bash
# Verificação básica
curl -f http://localhost:8000/healthcheck || echo "Aplicação com problemas"

# Verificação com timeout
timeout 5 curl http://localhost:8000/healthcheck
```

## 🐳 Docker

### Sobre o Dockerfile

O projeto utiliza um **multi-stage build** para otimizar a imagem Docker:

1. **Stage Development**: Usa `cgr.dev/chainguard/python:latest-dev` para instalar dependências
2. **Stage Production**: Usa `cgr.dev/chainguard/python:latest` (mais leve) para a imagem final


### Build e Execução

```bash
# Build da imagem
docker build -t moc-app .

# Execução com variáveis de ambiente
docker run -p 8000:8000 -e VERSION="1.0.0" moc-app
```

## 🚀 Deploy

### Variáveis de Ambiente
- `PORT`: Porta da aplicação (padrão: 8000)
- `HOST`: Host da aplicação (padrão: 0.0.0.0)
- `VERSION`: Versão da aplicação (opcional, usado pelo endpoint /version)
- `SQS_QUEUE_URL`: URL da fila SQS (obrigatório para endpoint /sent-message)

### Exemplo de deploy
```bash
# Usando uvicorn diretamente
uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Usando o script principal
python main.py

# Usando Docker
docker run -p 8000:8000 -e PORT=8000 -e VERSION="1.0.0" moc-app

# Usando Docker com SQS
docker run -p 8000:8000 \
  -e VERSION="1.0.0" \
  -e SQS_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue" \
  testapp
```

## 📝 Licença

Este projeto é apenas para fins de teste e demonstração pode ser reproduzido sem problemas mas não deve ser utilizado em produção. 