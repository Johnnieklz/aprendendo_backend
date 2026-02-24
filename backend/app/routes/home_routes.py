""" Rotas protegidas de aplicação """

from fastapi import APIRouter, Depends
from app.deps import get_current_user
from app.models.schemas import HomeResponse

router = APIRouter(prefix="/home", tags=["home"])

@router.get("", response_model=HomeResponse)
def home_endpoint(current_user=Depends(get_current_user)):
    """ Endpoint protegido que só responde para usuarios autenticados."""
    _ = current_user  # Apenas para evitar warning de variável não utilizada
    return {"message":  "Bem Vindo!"}