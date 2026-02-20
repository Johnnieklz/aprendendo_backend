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

# Se chegou aqui, é porque o email e CPF são únicos, então podemos criar o usuário.
    user_doc = {
        "nome": data.nome.strip(),
        "cpf": cpf_normalizado,
        "email": data.email.lower().strip(),
        "password_hash": hash_password(data.senha),
        "reset_token": None, 
    } 
    # Insere o novo usuário no banco de dados.
    insert_user(user_doc)
    return {"message": "Cadastro realizado com sucesso!!"}

def login_user(data: LoginRequest) -> dict:
    user = find_user_by_email(data.email)
    if not user or not verify_password(data.senha, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos!!"
        )
    access_token = create_access_token(subject=user["email"])
    return {"access_token": access_token, "token_type": "bearer"} 

def forgot_password(data: ForgortPasswordRequest) -> ForgortPasswordResponse:
    # levantamento sobre quais restrições precisam estar aqui - caso minimo;
    # Qual a lógica da restrição - não precisva de código, mas esquema;
    # Quais premissões/sucesso aconteceria após o processo de verificação - resposta de sucesso ou erro.
    user = find_user_by_email(data.email)
    if not user:
        # Para evitar expor quais emails estão cadastrados, retornamos uma mensagem genérica.
        return ForgortPasswordResponse(message="Se esse email estiver cadastrado, você receberá um email com instruções para resetar sua senha.")
    # Gerar um token de reset seguro.
    reset_token = secrets.token_urlsafe(32)
    # Salvar o token de reset no banco de dados associado ao usuário.
    update_user(user["email"], {"reset_token": reset_token})
 

def reset_password(data: ResetPasswordRequest) -> dict:
    # Levantamento sobre quais restrições precisam estar aqui - caso minimo;
    # Qual a lógica da restrição - não precisva de código, mas esquema;
    # Quais premissões/sucesso aconteceria após o processo de verificação - resposta.

    if data.nova_senha != data.confirmar_nova_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nova senha e confirmação não conferem!!"
        )
    user = find_user_by_reset_token(data.token.recuperacao)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="token de recuperação inválido!!"
        )
    # Atualizar a senha do usuário e limpar o token de reset.
    update_user(user["email"],{
        "password_hash": hash_password(data.nova_senha),
        "reset_token": None
        },
    )
    return {"message": "Senha alterada com sucesso!!"}