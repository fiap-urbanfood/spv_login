from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import (
    UsuarioSchemaBase,
    UsuarioSchemaCreate,
    UsuarioSchemaUp,
)
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()


# GET Logado
@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


# GET / Listar todos os usuários
@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios = result.scalars().unique().all()
        return usuarios


# POST / Signup
@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase
)
async def post_usuario(
    usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)
):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        eh_admin=usuario.eh_admin,
    )
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe um usuário com este email cadastrado.",
            )



# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')
    
    # Criar token de acesso
    token_acesso = criar_token_acesso(sub=str(usuario.id))
    
    return {
        "access_token": token_acesso,
        "token_type": "bearer"
    }