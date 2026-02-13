"""
Rotas publicas para autenticação de usuários.

-Todas as regras de negocio estarão aqui.

"""

import secrets
from fastapi import APIRouter, HTTPException, status

from app.services.config import settings
from app.services.database import (
    ForgortPasswordRequest,
    ForgortPasswordResponse,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    RegisterPasswordRequest,
    TokenResponse,
)

from app.services.database import (
    # Aqui vou importar todas as coisas que procuram no banco de dados.
    find_user_by_cpf,
    find_user_by_email,
    find_user_by_reset_token,
    insert_user,
    normalize_cpf,
    update_user,
)

from app.services.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

def register_user(data: RegisterRequest) -> dict: 
    if data.senha != data.confirmar_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha e confirmar senha não conferem!!"
        )
    
    cpf_normalizado = normalize_cpf(data.cpf)

    if find_user_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com esse email!!",
        )
    
    if find_user_by_cpf(cpf_normalizado):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com esse CPF!!"
        )