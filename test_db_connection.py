import asyncio
import aiosqlite


async def test_connection():
    try:
        conn = await aiosqlite.connect("local.db")
        print("Conexão SQLite bem-sucedida!")
        await conn.close()
    except Exception as e:
        print(f"Erro ao conectar: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
