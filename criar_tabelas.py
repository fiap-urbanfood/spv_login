from core.configs import settings
from core.database import engine


async def create_tables() -> None:
    import models.__all_models

    print("Criando as tabelas no banco de dados")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print("Tabelas criadas com sucesso...")


async def main():
    try:
        await create_tables()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
