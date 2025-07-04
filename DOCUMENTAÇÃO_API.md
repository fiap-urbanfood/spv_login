# Documentação da API - Microserviço de Usuários

## Visão Geral

Este documento descreve como aplicações externas podem interagir com o microserviço de autenticação e gerenciamento de usuários do Sistema de Processamento de Vídeo (SPV).

## Informações Básicas

- **URL Base**: `http://localhost:8000` (desenvolvimento)
- **Versão da API**: v1
- **Prefixo da API**: `/api/v1`
- **Autenticação**: JWT Bearer Token
- **Formato de Resposta**: JSON

## Autenticação

O microserviço utiliza autenticação JWT (JSON Web Token) com as seguintes características:

- **Algoritmo**: HS256
- **Duração do Token**: 7 dias (10080 minutos)
- **Tipo**: Bearer Token

### Como obter um token de acesso

Para acessar endpoints protegidos, você precisa primeiro fazer login e obter um token de acesso.

## Endpoints Disponíveis

### 1. Autenticação

#### POST `/api/v1/usuarios/login`

Realiza o login do usuário e retorna um token de acesso.

**Parâmetros:**
- `username` (string): Email do usuário
- `password` (string): Senha do usuário

**Exemplo de requisição:**
```bash
curl -X POST "http://localhost:8000/api/v1/usuarios/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@exemplo.com&password=minhasenha"
```

**Resposta de sucesso (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Resposta de erro (400):**
```json
{
  "detail": "Dados de acesso incorretos."
}
```

### 2. Gerenciamento de Usuários

#### GET `/api/v1/usuarios/`

Lista todos os usuários cadastrados no sistema.

**Autenticação:** Não requerida

**Exemplo de requisição:**
```bash
curl -X GET "http://localhost:8000/api/v1/usuarios/"
```

**Resposta de sucesso (200):**
```json
[
  {
    "id": 1,
    "nome": "João",
    "sobrenome": "Silva",
    "email": "joao@exemplo.com",
    "eh_admin": false
  },
  {
    "id": 2,
    "nome": "Maria",
    "sobrenome": "Santos",
    "email": "maria@exemplo.com",
    "eh_admin": true
  }
]
```

#### GET `/api/v1/usuarios/logado`

Retorna informações do usuário atualmente autenticado.

**Autenticação:** Obrigatória (Bearer Token)

**Exemplo de requisição:**
```bash
curl -X GET "http://localhost:8000/api/v1/usuarios/logado" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Resposta de sucesso (200):**
```json
{
  "id": 1,
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@exemplo.com",
  "eh_admin": false
}
```

**Resposta de erro (401):**
```json
{
  "detail": "Not authenticated"
}
```

#### POST `/api/v1/usuarios/signup`

Cria um novo usuário no sistema.

**Autenticação:** Não requerida

**Corpo da requisição:**
```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@exemplo.com",
  "senha": "minhasenha123",
  "eh_admin": false
}
```

**Exemplo de requisição:**
```bash
curl -X POST "http://localhost:8000/api/v1/usuarios/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João",
    "sobrenome": "Silva",
    "email": "joao@exemplo.com",
    "senha": "minhasenha123",
    "eh_admin": false
  }'
```

**Resposta de sucesso (201):**
```json
{
  "id": 3,
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@exemplo.com",
  "eh_admin": false
}
```

**Resposta de erro (406):**
```json
{
  "detail": "Já existe um usuário com este email cadastrado."
}
```

## Estrutura de Dados

### Usuário (UsuarioSchemaBase)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | integer | Não | ID único do usuário (gerado automaticamente) |
| nome | string | Sim | Nome do usuário |
| sobrenome | string | Sim | Sobrenome do usuário |
| email | string | Sim | Email do usuário (deve ser válido) |
| eh_admin | boolean | Não | Indica se o usuário é administrador (padrão: false) |

### Criação de Usuário (UsuarioSchemaCreate)

Estende `UsuarioSchemaBase` e adiciona:
- `senha` (string, obrigatório): Senha do usuário (será criptografada)

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Autenticação necessária |
| 406 | Not Acceptable - Conflito de dados (ex: email já existe) |
| 500 | Internal Server Error - Erro interno do servidor |

## Exemplos de Uso em Diferentes Linguagens

### JavaScript (Fetch API)

```javascript
// Login
async function login(email, password) {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await fetch('http://localhost:8000/api/v1/usuarios/login', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  return data.access_token;
}

// Listar usuários
async function getUsers() {
  const response = await fetch('http://localhost:8000/api/v1/usuarios/');
  return await response.json();
}

// Obter usuário logado
async function getCurrentUser(token) {
  const response = await fetch('http://localhost:8000/api/v1/usuarios/logado', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
}
```

### Python (requests)

```python
import requests

# Login
def login(email, password):
    data = {
        'username': email,
        'password': password
    }
    response = requests.post('http://localhost:8000/api/v1/usuarios/login', data=data)
    return response.json()['access_token']

# Listar usuários
def get_users():
    response = requests.get('http://localhost:8000/api/v1/usuarios/')
    return response.json()

# Obter usuário logado
def get_current_user(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:8000/api/v1/usuarios/logado', headers=headers)
    return response.json()
```

### cURL

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/usuarios/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@exemplo.com&password=senha123"

# Listar usuários
curl -X GET "http://localhost:8000/api/v1/usuarios/"

# Obter usuário logado
curl -X GET "http://localhost:8000/api/v1/usuarios/logado" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## Configuração de Produção

Para usar em produção, certifique-se de:

1. **Alterar a URL base** para o domínio do seu servidor
2. **Configurar HTTPS** para segurança
3. **Ajustar as configurações de CORS** se necessário
4. **Usar variáveis de ambiente** para configurações sensíveis
5. **Configurar um banco de dados de produção** (MySQL RDS)

## Segurança

- As senhas são criptografadas usando hash antes de serem armazenadas
- Tokens JWT têm expiração de 7 dias
- Endpoints sensíveis requerem autenticação
- Validação de email é realizada automaticamente

## Suporte

Para dúvidas ou problemas com a API, consulte:
- Especificação OpenAPI gerada automaticamente: `http://localhost:8000/docs`
- Interface interativa Swagger: `http://localhost:8000/redoc`

## Notas Importantes

1. **Tokens JWT**: Guarde os tokens de forma segura e não os compartilhe
2. **Expiração**: Tokens expiram após 7 dias, renove quando necessário
3. **Email único**: Cada email pode ser usado apenas uma vez no sistema
4. **Admin**: Apenas usuários com `eh_admin: true` têm privilégios administrativos
5. **Banco de dados**: O sistema usa MySQL RDS na AWS por padrão 