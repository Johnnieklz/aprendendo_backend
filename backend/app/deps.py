"""
Dependências reutilizáveis para injeção de dependências em rotas FastAPI.

Este arquivo concentra a lógica de autenticação para usar em múltiplas rotas.

"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.database import find_user_by_id
from app.services.security import decode_access_token

# Esquema padrão para token Bearer no header Authorization.
bearer_sheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_sheme),):
    """ Retorna usuário autenticado a partir de JWT 
         Se o token ausente/inválido, levanta HTTPException 401.
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não informado."
        )
    payload = decode_access_token(credentials.credentials)
    email = payload.get("sub")
    user = find_user_by_id(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado."
        ) 
    return user
