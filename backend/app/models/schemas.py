"""
Modelos  de Entrada e saida da API

 - Esses modelos validam osd ados automaticamente e deixam o código mais legivel.
 
 - Nosso login terá Nome, CPF, Email, senha e confirmar senha.
"""
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    # Dados recebidos para cadastrar um novo usuário
    nome: str = Field(min_length=2, max_length=150) # O nome deve ter entre 2 e 150 caracteres
    cpf: str = Field(min_length=11, max_length=14) # O CPF deve ter entre 11 e 14 caracteres (considerando pontos e traços)
    email: EmailStr # Valida automaticamente se o email é válido
    senha: str = Field(min_length=6, max_length=128) # A senha deve ter entre 6 e 128 caracteres
    confirmar_senha: str = Field(min_length=6, max_length=128) # Para confirmar a senha, deve ser igual a senha

# Modelo para login, onde o usuário pode usar email ou cpf para se autenticar

class LoginRequest(BaseModel):
    # Dados recebidos para autenticar um usuário.
    email: EmailStr
    senha: str = Field(min_length=6, max_length=128)

# Modelo para recuperar senha.
class ForgotPasswordRequest(BaseModel):
    # Entrada da rota de esqueci senha.
    email: EmailStr

# Modelo para criar um token de reset de senha.
class TokenResponse(BaseModel):
    # Resposta padrão de login contendo um token JWT.
    access_token: str
    token_type: str = "bearer" # O tipo do token, geralmente "bearer" para tokens JWT.


# Modelo para resposta de mensagens simples.
class MessageResponse(BaseModel):
    # Resposta simples de mensagem.
    message: str 

class ForgotPasswordResponse(BaseModel):
    # Resposta da rota de esqueci senha.
    # O 'token_debug' só aparece em ambiente de desenvolvimento local.
    message: str
    token_debug: str | None = None # por que none? Porque em produção não queremos expor o token de reset, mas em desenvolvimento pode ser útil para testes.

class HomeResponse(BaseModel):
    # Resposta da rota home, apenas para testar se a autenticação funciona.
    message: str