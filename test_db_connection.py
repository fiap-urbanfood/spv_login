import asyncio
import aiomysql
from urllib.parse import quote_plus


async def test_connection():
    try:
        # MySQL RDS Configuration
        host = "rds-mysql.c8gkm8vsq6yc.us-east-1.rds.amazonaws.com"
        port = 3306
        user = "urbanfood"
        password = "Urbanf00dFiap"
        db = "urbanfood"
        
        print("Tentando conectar...")
        conn = await aiomysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db
        )
        print("Conexão MySQL RDS bem-sucedida!")
        await conn.ensure_closed()
    except Exception as e:
        print(f"Erro ao conectar: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
