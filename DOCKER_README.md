# Docker - Microserviço de Login SPV

Este documento explica como executar o microserviço de login usando Docker.

## Pré-requisitos

- Docker instalado

## Execução com Dockerfile

### 1. Build da Imagem

```bash
# Build da imagem
docker build -t spv-login-api .

# Build sem cache (se necessário)
docker build --no-cache -t spv-login-api .
```

### 2. Execução do Container

```bash
# Execução básica
docker run -p 8000:8000 spv-login-api

# Execução em background
docker run -d -p 8000:8000 --name spv-login-container spv-login-api

# Execução com restart automático
docker run -d -p 8000:8000 --restart unless-stopped --name spv-login-container spv-login-api
```

### 3. Execução com Variáveis de Ambiente

```bash
# Executar com configurações personalizadas
docker run -d -p 8000:8000 \
  --name spv-login-container \
  -e DB_HOST=seu-host-mysql \
  -e DB_NAME=seu-banco \
  -e DB_USERNAME=seu-usuario \
  -e DB_PASSWORD=sua-senha \
  -e JWT_SECRET=sua-chave-secreta \
  spv-login-api
```

## Comandos Úteis

### Gerenciamento de Containers

```bash
# Ver containers em execução
docker ps

# Ver logs do container
docker logs spv-login-container

# Ver logs em tempo real
docker logs -f spv-login-container

# Parar container
docker stop spv-login-container

# Remover container
docker rm spv-login-container

# Parar e remover em um comando
docker rm -f spv-login-container
```

### Gerenciamento de Imagens

```bash
# Listar imagens
docker images

# Remover imagem
docker rmi spv-login-api

# Forçar remoção
docker rmi -f spv-login-api
```

## Variáveis de Ambiente

### Configuração do Banco de Dados

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DB_HOST` | `rds-mysql.c8gkm8vsq6yc.us-east-1.rds.amazonaws.com` | Host do banco MySQL |
| `DB_NAME` | `urbanfood` | Nome do banco de dados |
| `DB_USERNAME` | `urbanfood` | Usuário do banco |
| `DB_PASSWORD` | `Urbanf00dFiap` | Senha do banco |
| `DB_PORT` | `3306` | Porta do banco |

### Configuração JWT

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `JWT_SECRET` | `P7pK6xHhw04VMybl0VqeYIaGXWnJuADzQQw-pY1rwP8` | Chave secreta para JWT |
| `ALGORITHM` | `HS256` | Algoritmo de criptografia |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` | Duração do token (7 dias) |

### Arquivo .env (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados
DB_HOST=seu-host-mysql
DB_NAME=seu-banco
DB_USERNAME=seu-usuario
DB_PASSWORD=sua-senha
DB_PORT=3306

# JWT
JWT_SECRET=sua-chave-secreta-muito-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

E execute com:

```bash
docker run -d -p 8000:8000 \
  --env-file .env \
  --name spv-login-container \
  spv-login-api
```

## Portas

- **8000**: API FastAPI (http://localhost:8000)

## Endpoints Disponíveis

Após executar o container, acesse:

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/usuarios/

## Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco**
   ```bash
   # Verificar logs
   docker logs spv-login-container
   
   # Executar com shell para debug
   docker run -it --rm spv-login-api /bin/bash
   ```

2. **Porta já em uso**
   ```bash
   # Verificar processos na porta 8000
   lsof -i :8000
   
   # Parar processo
   kill -9 PID
   
   # Ou usar porta diferente
   docker run -p 8001:8000 spv-login-api
   ```

3. **Permissões de arquivo**
   ```bash
   # Rebuild sem cache
   docker build --no-cache -t spv-login-api .
   ```

### Debug

```bash
# Executar com shell interativo
docker run -it --rm spv-login-api /bin/bash

# Executar com debug Python
docker run -p 8000:8000 \
  -e PYTHONPATH=/app \
  spv-login-api \
  python -m debugpy --listen 0.0.0.0:5678 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Desenvolvimento

### Modo Desenvolvimento com Volume

Para desenvolvimento com hot-reload:

```bash
# Executar com volume para código
docker run -p 8000:8000 \
  -v $(pwd):/app \
  -e PYTHONPATH=/app \
  spv-login-api \
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Executar Scripts Específicos

```bash
# Executar script de criação de tabelas
docker run --rm spv-login-api python criar_tabelas.py

# Executar script de população
docker run --rm spv-login-api python popular_usuarios.py

# Testar conexão com banco
docker run --rm spv-login-api python test_db_connection.py
```

## Produção

### Build Otimizado

```bash
# Build para produção
docker build -t spv-login-api:prod .

# Tag para registry
docker tag spv-login-api:prod seu-registry/spv-login-api:latest
```

### Deploy

```bash
# Executar em produção
docker run -d \
  --name spv-login-api-prod \
  -p 8000:8000 \
  --restart unless-stopped \
  -e DB_HOST=prod-host \
  -e DB_PASSWORD=prod-password \
  spv-login-api:prod
```

### Push para Registry

```bash
# Push para Docker Hub
docker push seu-registry/spv-login-api:latest

# Push para registry privado
docker push registry.empresa.com/spv-login-api:latest
```

## Monitoramento

### Logs

```bash
# Logs em tempo real
docker logs -f spv-login-container

# Últimas 100 linhas
docker logs --tail=100 spv-login-container

# Logs com timestamp
docker logs -t spv-login-container
```

### Métricas

```bash
# Estatísticas do container
docker stats spv-login-container

# Uso de recursos
docker system df

# Informações detalhadas
docker inspect spv-login-container
```

## Exemplos Completos

### Desenvolvimento Local

```bash
# 1. Build da imagem
docker build -t spv-login-api .

# 2. Executar com banco RDS
docker run -d -p 8000:8000 \
  --name spv-login-dev \
  --restart unless-stopped \
  spv-login-api

# 3. Verificar logs
docker logs -f spv-login-dev

# 4. Acessar API
curl http://localhost:8000/api/v1/usuarios/
```

### Produção

```bash
# 1. Build para produção
docker build -t spv-login-api:prod .

# 2. Executar em produção
docker run -d \
  --name spv-login-prod \
  -p 8000:8000 \
  --restart unless-stopped \
  -e DB_HOST=prod-mysql.empresa.com \
  -e DB_NAME=spv_prod \
  -e DB_USERNAME=spv_user \
  -e DB_PASSWORD=senha_segura_prod \
  -e JWT_SECRET=chave_super_secreta_producao \
  spv-login-api:prod

# 3. Monitorar
docker logs -f spv-login-prod
``` 