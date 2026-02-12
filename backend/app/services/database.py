"""
Acesso ao banco de dados TinyDB para operações relacionadas à autenticação de usuários.

- Um banco NOSQL baseado em arquivos JSON.
"""

from tinydb import TinyDB, Query
from app.config import settings


# Instancia global do banco de dados, apontando para um arquivo JSON

db = TinyDB(settings.database_path)
users_table = db.table("users")

def find_user_by_email(email: str):
    # Retorna um usuário por meio do email ou None se não encontrado.
    user_query = Query()
    return users_table.get(user_query.email == email.lower().strip())

def find_user_by_cpf(cpf: str):
    # Retorna um usuário por meio do CPF ou None se não encontrado.
    user_query = Query()
    return users_table.get(user_query.cpf == normalize_cpf(cpf))

def find_user_by_reset_token(token: str):
    # Busca um usuário por meio do token de recuperação de senha.
    user = Query()
    return users_table.get(user.reset_token == token)

def insert_user(user_data: dict):
    # Insere um novo usuário na "tabela" users.
    users_table.insert(user_data)

    def update_user(email_str, updates: dict):
        # Atualizar usuario por meio do email.
        users_query = Query()
        users_table.update(updates, users_query.email == email_str.lower().strip())

def normalize_cpf(cpf: str):
    # Remove caracteres não numericos do CPF para facilitar a busca.
    # exemplo: "123.456.789-00" -> "12345678900"
    return "".join(char for char in cpf if char.isdigit())