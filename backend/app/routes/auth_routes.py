"""
Rotas publicas para autenticação de usuários.

-Todas as regras de negocio estarão aqui.

"""

import secrets
from fastapi import APIRouter, HTTPException, status

from app.config import settings 
from app.models.schemas import{
    ForgortPasswordRequest,
    ForgortPasswordResponse,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    RegisterPasswordRequest,
    TokenResponse,
}

from app.sevices.database import{
    # Aqui vou importar todas as coisas que procuram no banco de dados.
    find_user_by_cpf,
    find_user_by_email,
    find_user_by_reset_token,
    insert_user,
    normalize_cpf,
    update_user,
}

from app.services.security import create_access_token, hash_password, verify_password