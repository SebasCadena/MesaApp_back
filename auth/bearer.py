from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth import verify_token
from app.models.user_model import User
from config.config import get_db
from sqlalchemy.orm import Session

security = HTTPBearer(auto_error=True)

def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependencia que verifica access token JWT en cada petición protegida.
    Extrae el token del header 'Authorization: Bearer <token>'
    """
    token = credentials.credentials
    payload = verify_token(token, expected_type="access")
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


def get_current_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> User:
    """Resuelve el usuario autenticado y activo desde el claim sub del token."""
    user_id = payload.get("sub")
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.get(User, user_id_int)
    if user is None or not user.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo o no existe")

    return user