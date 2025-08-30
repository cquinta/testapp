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

## ⚠️ Avisos Importantes

- Os endpoints `/cpu/{duration_seconds}` e `/mem/{duration_seconds}` podem causar alta utilização de recursos
- O endpoint `/healthtime` muda comportamento após 60 segundos de execução
- O endpoint `/version` requer a variável de ambiente VERSION definida
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
- **psutil**: Monitoramento de recursos do sistema

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

**Benefícios:**
- Imagem final menor (sem ferramentas de desenvolvimento)
- Maior segurança (imagens Chainguard são distroless)
- Ambiente virtual isolado para dependências

### Build e Execução

```bash
# Build da imagem
docker build -t testapp .

# Execução com variáveis de ambiente
docker run -p 8000:8000 -e VERSION="1.0.0" testapp
```

## 🚀 Deploy

### Variáveis de Ambiente
- `PORT`: Porta da aplicação (padrão: 8000)
- `HOST`: Host da aplicação (padrão: 0.0.0.0)
- `VERSION`: Versão da aplicação (opcional, usado pelo endpoint /version)

### Exemplo de deploy
```bash
# Usando uvicorn diretamente
uvicorn app:app --host 0.0.0.0 --port $PORT

# Usando Docker
docker run -p 8000:8000 -e PORT=8000 testapp
```

## 📝 Licença

Este projeto é apenas para fins de teste e demonstração pode ser reproduzido sem problemas mas não deve ser utilizado em produção. 