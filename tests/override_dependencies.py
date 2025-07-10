from typing import AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from core.deps import get_session

def get_test_session(session: AsyncSession) -> Callable:
    """Sobrescreve a dependência de sessão do banco de dados para os testes"""
    async def override_session() -> AsyncGenerator[AsyncSession, None]:
        yield session
    return override_session

def override_dependencies(session: AsyncSession) -> None:
    """Configura as dependências para os testes"""
    app.dependency_overrides[get_session] = get_test_session(session) 