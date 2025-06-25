import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import Session
from core.security import gerar_hash_senha
from models.usuario_model import UsuarioModel

# Lista de usuários para popular o banco
usuarios_exemplo = [
    {
        "nome": "João",
        "sobrenome": "Silva",
        "email": "joao.silva@exemplo.com",
        "senha": "senha123",
        "eh_admin": True
    },
    {
        "nome": "Maria",
        "sobrenome": "Santos",
        "email": "maria.santos@exemplo.com",
        "senha": "senha456",
        "eh_admin": False
    },
    {
        "nome": "Pedro",
        "sobrenome": "Oliveira",
        "email": "pedro.oliveira@exemplo.com",
        "senha": "senha789",
        "eh_admin": False
    },
    {
        "nome": "Ana",
        "sobrenome": "Costa",
        "email": "ana.costa@exemplo.com",
        "senha": "senha101",
        "eh_admin": True
    },
    {
        "nome": "Carlos",
        "sobrenome": "Pereira",
        "email": "carlos.pereira@exemplo.com",
        "senha": "senha202",
        "eh_admin": False
    },
    {
        "nome": "Lucia",
        "sobrenome": "Ferreira",
        "email": "lucia.ferreira@exemplo.com",
        "senha": "senha303",
        "eh_admin": False
    },
    {
        "nome": "Roberto",
        "sobrenome": "Almeida",
        "email": "roberto.almeida@exemplo.com",
        "senha": "senha404",
        "eh_admin": False
    },
    {
        "nome": "Fernanda",
        "sobrenome": "Lima",
        "email": "fernanda.lima@exemplo.com",
        "senha": "senha505",
        "eh_admin": True
    },
    {
        "nome": "Ricardo",
        "sobrenome": "Gomes",
        "email": "ricardo.gomes@exemplo.com",
        "senha": "senha606",
        "eh_admin": False
    },
    {
        "nome": "Patricia",
        "sobrenome": "Ribeiro",
        "email": "patricia.ribeiro@exemplo.com",
        "senha": "senha707",
        "eh_admin": False
    }
]

async def popular_usuarios():
    session: AsyncSession = Session()
    
    try:
        async with session as db:
            # Verificar se já existem usuários
            query = select(UsuarioModel)
            result = await db.execute(query)
            usuarios_existentes = result.scalars().unique().all()
            
            if usuarios_existentes:
                print(f"Já existem {len(usuarios_existentes)} usuários no banco.")
                print("Deseja continuar mesmo assim? (s/n): ", end="")
                resposta = input().lower()
                if resposta != 's':
                    print("Operação cancelada.")
                    return
            
            print("Iniciando população do banco de dados...")
            
            for i, dados_usuario in enumerate(usuarios_exemplo, 1):
                # Criar hash da senha
                senha_hash = gerar_hash_senha(dados_usuario["senha"])
                
                # Criar usuário
                novo_usuario = UsuarioModel(
                    nome=dados_usuario["nome"],
                    sobrenome=dados_usuario["sobrenome"],
                    email=dados_usuario["email"],
                    senha=senha_hash,
                    eh_admin=dados_usuario["eh_admin"]
                )
                
                db.add(novo_usuario)
                print(f"Usuário {i}: {dados_usuario['nome']} {dados_usuario['sobrenome']} - {dados_usuario['email']}")
            
            await db.commit()
            print(f"\n✅ {len(usuarios_exemplo)} usuários criados com sucesso!")
            print("\nCredenciais para teste:")
            print("=" * 50)
            for dados in usuarios_exemplo:
                print(f"Email: {dados['email']}")
                print(f"Senha: {dados['senha']}")
                print(f"Admin: {'Sim' if dados['eh_admin'] else 'Não'}")
                print("-" * 30)
                
    except Exception as e:
        print(f"❌ Erro ao popular usuários: {e}")
        await db.rollback()

if __name__ == "__main__":
    asyncio.run(popular_usuarios()) 