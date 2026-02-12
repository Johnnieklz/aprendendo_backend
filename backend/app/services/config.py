"""
Configurações gerais do projeto

- Este arquivo concentra valores de ambiente para evitar valores sensiveis espalhados no código.
"""

from pathlib import Path
from pydantic import BaseModel

#Diretorio raiz do backend
BACK_ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseModel):
    # Representar as configurações de execução da API.

    # Chave usada para assinar JWT. 
    # Quando colocarmos isso em produção, devemos trocar esse valor por uma variável de ambiente segura.
    secret_key = str = "CHANGE_ME_SUPER_KEY_FOR_CLASSROOM"

    # Algoritmo de assinatura do JWT.
    algorithm = str = "HS256"

    # Tempo de expiração do token em minutos.
    Access_token_expire_minutes = int = 30

    # Arquivo JSON do TinyDB
    database_path = str = str(BACK_ROOT/"DATA"/"db.json")

    # Quando isso for True, devemos expor o token de recuperação de senha na resposta.
    # Super útel apenas para aprendizado.
    debug_password_reset_token = bool = True

# Instancia global das configurações
settings = Settings()