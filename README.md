# Test Application API

Uma API FastAPI para testes de healthcheck, fault injection e stress testing de CPU.

> **Nota**: Esta é uma tentativa de criar uma versão em Python com funcionalidades semelhantes ao aplicativo em Go "chip", encontrado em https://github.com/msfidelis/chip

## 📋 Visão Geral

Esta aplicação fornece endpoints para simular diferentes cenários de teste, incluindo:
- Healthchecks básicos e com falhas
- Fault injection com diferentes probabilidades
- Stress testing de CPU
- Informações do servidor

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
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Usando Docker

```bash
docker build -t testapp .
docker run -p 8000:8000 testapp
```

## 📖 Documentação da API

A documentação interativa está disponível em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Endpoints

### Info
- `GET /` - Retorna o hostname do servidor

### Health
- `GET /healthcheck` - Healthcheck básico (sempre retorna 200)
- `GET /healthcheck/error` - Sempre retorna erro 500
- `GET /healthtime` - Retorna sucesso por 60s, depois erro 500

### Fault Injection
- `GET /healthcheck/fault` - Retorna aleatoriamente 200 ou 503 (50% cada)
- `GET /healthcheck/fault/soft` - Retorna 200 (87.5%) ou 503 (12.5%)

### Performance
- `GET /cpu/{duration_seconds}` - Executa stress test de CPU pelo tempo especificado

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

## ⚠️ Avisos Importantes

- O endpoint `/cpu/{duration_seconds}` pode causar alta utilização de CPU
- O endpoint `/healthtime` muda comportamento após 60 segundos de execução
- Use os endpoints de fault injection para simular falhas em testes

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
testapp/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências Python
├── Dockerfile         # Configuração Docker
└── README.md          # Este arquivo
```

### Dependências
- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validação de dados

## 📊 Monitoramento

Para monitorar a aplicação, você pode usar os endpoints de healthcheck:

```bash
# Verificação básica
curl -f http://localhost:8000/healthcheck || echo "Aplicação com problemas"

# Verificação com timeout
timeout 5 curl http://localhost:8000/healthcheck
```

## 🐳 Deploy

### Variáveis de Ambiente
- `PORT`: Porta da aplicação (padrão: 8000)
- `HOST`: Host da aplicação (padrão: 0.0.0.0)

### Exemplo de deploy
```bash
# Usando uvicorn diretamente
uvicorn app:app --host 0.0.0.0 --port $PORT

# Usando Docker
docker run -p 8000:8000 -e PORT=8000 testapp
```

## 📝 Licença

Este projeto é apenas para fins de teste e demonstração.