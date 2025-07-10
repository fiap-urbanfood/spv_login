# Guia de Testes - Microserviço de Login SPV

Este documento explica como executar e criar testes para o microserviço de login.

## 📋 Índice

1. [Configuração do Ambiente](#configuração-do-ambiente)
2. [Estrutura dos Testes](#estrutura-dos-testes)
3. [Executando os Testes](#executando-os-testes)
4. [Criando Novos Testes](#criando-novos-testes)
5. [Fixtures Disponíveis](#fixtures-disponíveis)
6. [Exemplos Práticos](#exemplos-práticos)

## 🔧 Configuração do Ambiente

### Pré-requisitos

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Dependências Principais para Testes

- `pytest`: Framework de testes
- `pytest-asyncio`: Suporte para testes assíncronos
- `httpx`: Cliente HTTP assíncrono
- `aiosqlite`: Banco SQLite assíncrono para testes

## 📁 Estrutura dos Testes

```
tests/
├── __init__.py
├── conftest.py              # Configurações e fixtures globais
├── override_dependencies.py # Sobrescrita de dependências
└── test_usuario_endpoints.py # Testes dos endpoints
```

### Arquivos Principais

1. **conftest.py**: Configuração global dos testes
   - Configuração do banco de dados
   - Fixtures comuns
   - Setup e teardown

2. **override_dependencies.py**: Gerenciamento de dependências
   - Sobrescrita de dependências para testes
   - Configuração de injeção de dependências

3. **test_usuario_endpoints.py**: Testes dos endpoints
   - Testes de criação de usuário
   - Testes de autenticação
   - Testes de listagem

## ▶️ Executando os Testes

### Executar Todos os Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Com cobertura de código
pytest tests/ -v --cov=.

# Com relatório detalhado
pytest tests/ -v --cov=. --cov-report=html
```

### Executar Testes Específicos

```bash
# Executar um arquivo específico
pytest tests/test_usuario_endpoints.py -v

# Executar um teste específico
pytest tests/test_usuario_endpoints.py::test_criar_usuario -v

# Executar testes que contenham uma palavra específica
pytest -k "criar" -v
```

## 🆕 Criando Novos Testes

### 1. Estrutura Básica de um Teste

```python
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_novo_endpoint(client: AsyncClient):
    response = await client.get("/api/v1/seu-endpoint")
    assert response.status_code == 200
    data = response.json()
    assert "chave_esperada" in data
```

### 2. Usando Fixtures

```python
async def test_com_fixtures(
    client: AsyncClient,
    usuario_teste: dict,
    token_acesso: str
):
    headers = {"Authorization": f"Bearer {token_acesso}"}
    response = await client.get("/api/v1/endpoint", headers=headers)
    assert response.status_code == 200
```

### 3. Testando Erros

```python
async def test_erro_validacao(client: AsyncClient):
    dados_invalidos = {
        "email": "email_invalido",
        "senha": "123"
    }
    response = await client.post("/api/v1/usuarios/signup", json=dados_invalidos)
    assert response.status_code == 422  # Erro de validação
```

## 🛠️ Fixtures Disponíveis

### Banco de Dados

```python
@pytest.fixture
async def db_session(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    """Cria uma sessão do banco de dados"""
    async with async_session_maker() as session:
        yield session
        await session.close()
```

### Cliente HTTP

```python
@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP assíncrono para testes"""
    override_dependencies(db_session)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

### Dados de Teste

```python
@pytest.fixture
def usuario_teste() -> dict:
    """Dados de usuário para teste"""
    return {
        "nome": "Teste",
        "sobrenome": "Usuario",
        "email": "teste@example.com",
        "senha": "senha123",
        "eh_admin": False
    }
```

## 📝 Exemplos Práticos

### 1. Teste de Criação de Usuário

```python
async def test_criar_usuario(client: AsyncClient, usuario_teste: dict):
    response = await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == usuario_teste["email"]
    assert "senha" not in data
```

### 2. Teste de Autenticação

```python
async def test_login_sucesso(client: AsyncClient, usuario_teste: dict):
    # Criar usuário
    await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    
    # Fazer login
    login_data = {
        "username": usuario_teste["email"],
        "password": usuario_teste["senha"]
    }
    response = await client.post("/api/v1/usuarios/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### 3. Teste com Autenticação

```python
async def test_endpoint_autenticado(
    client: AsyncClient,
    token_acesso: str
):
    headers = {"Authorization": f"Bearer {token_acesso}"}
    response = await client.get("/api/v1/usuarios/logado", headers=headers)
    assert response.status_code == 200
```

## 🔍 Dicas e Boas Práticas

1. **Isolamento de Testes**
   - Cada teste deve ser independente
   - Use fixtures para setup e teardown
   - Evite dependências entre testes

2. **Nomeação de Testes**
   - Use nomes descritivos
   - Siga o padrão `test_<funcionalidade>_<cenario>`
   - Documente casos complexos

3. **Asserções**
   - Verifique status code
   - Valide estrutura da resposta
   - Teste casos de erro

4. **Banco de Dados**
   - Use banco em memória para testes
   - Limpe dados entre testes
   - Evite dependência de dados externos

5. **Autenticação**
   - Teste endpoints protegidos
   - Verifique diferentes níveis de acesso
   - Teste tokens inválidos/expirados

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de Conexão com Banco**
   ```bash
   # Verificar se o banco de testes está configurado
   pytest --setup-show tests/
   ```

2. **Testes Assíncronos Falhando**
   ```bash
   # Executar com debug
   pytest -v --log-cli-level=DEBUG tests/
   ```

3. **Conflitos de Dependência**
   ```bash
   # Limpar cache do pytest
   pytest --cache-clear tests/
   ```

## 📚 Recursos Adicionais

- [Documentação do Pytest](https://docs.pytest.org/)
- [Documentação do FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Documentação do SQLAlchemy Async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)

## 🤝 Contribuindo

1. Crie testes para novas funcionalidades
2. Mantenha a cobertura de código alta
3. Documente casos especiais
4. Siga os padrões existentes
5. Execute a suite completa antes de commits 