import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_criar_usuario(client: AsyncClient, usuario_teste: dict):
    response = await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == usuario_teste["email"]
    assert data["nome"] == usuario_teste["nome"]
    assert "senha" not in data

async def test_criar_usuario_email_duplicado(client: AsyncClient, usuario_teste: dict):
    # Criar primeiro usuário
    response = await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    assert response.status_code == 201

    # Tentar criar usuário com mesmo email
    response = await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    assert response.status_code == 406
    assert "Já existe um usuário com este email cadastrado" in response.json()["detail"]

async def test_login_sucesso(client: AsyncClient, usuario_teste: dict):
    # Criar usuário
    response = await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    assert response.status_code == 201

    # Fazer login
    login_data = {
        "username": usuario_teste["email"],
        "password": usuario_teste["senha"]
    }
    response = await client.post("/api/v1/usuarios/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_falha(client: AsyncClient):
    login_data = {
        "username": "naoexiste@example.com",
        "password": "senhaerrada"
    }
    response = await client.post("/api/v1/usuarios/login", data=login_data)
    assert response.status_code == 400
    assert "Dados de acesso incorretos" in response.json()["detail"]

async def test_get_usuarios(client: AsyncClient, usuario_teste: dict):
    # Criar um usuário
    response = await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    assert response.status_code == 201

    # Listar usuários
    response = await client.get("/api/v1/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["email"] == usuario_teste["email"]

@pytest.fixture
async def token_acesso(client: AsyncClient, usuario_teste: dict) -> str:
    # Criar usuário
    response = await client.post("/api/v1/usuarios/signup", json=usuario_teste)
    assert response.status_code == 201
    
    # Fazer login
    login_data = {
        "username": usuario_teste["email"],
        "password": usuario_teste["senha"]
    }
    response = await client.post("/api/v1/usuarios/login", data=login_data)
    return response.json()["access_token"]

async def test_get_usuario_logado(client: AsyncClient, usuario_teste: dict, token_acesso: str):
    # Tentar acessar sem token
    response = await client.get("/api/v1/usuarios/logado")
    assert response.status_code == 401

    # Acessar com token
    headers = {"Authorization": f"Bearer {token_acesso}"}
    response = await client.get("/api/v1/usuarios/logado", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == usuario_teste["email"] 