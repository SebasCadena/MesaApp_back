from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.auth_schema import (
    AccessTokenResponse,
    AuthUserResponse,
    LoginRequest,
    MeResponse,
    RefreshTokenRequest,
    TokenResponse,
)
from auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
)
from auth.bearer import get_current_user
from auth.roles import get_user_security_context
from config.config import get_db

router = APIRouter(prefix="/auth", tags=["autenticación"])


def _build_auth_user(user: User, context: dict) -> AuthUserResponse:
    return AuthUserResponse(
        id=user.id,
        nombre=user.nombre,
        cedula=user.cedula,
        correo=user.correo,
        tienda_id=context["store_id"],
        is_superadmin=context["is_superadmin"],
        roles=context["roles"],
        permisos=context["permissions"],
    )


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Autentica por cédula y retorna access/refresh tokens."""
    user = db.query(User).filter(User.cedula == login_data.cedula).first()

    if user is None or not user.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    context = get_user_security_context(db=db, user_id=user.id)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "cedula": user.cedula,
            "store_id": context["store_id"],
            "is_superadmin": context["is_superadmin"],
        },
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id), "cedula": user.cedula})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": _build_auth_user(user, context),
    }


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Genera un nuevo access token a partir de un refresh token válido."""
    payload = verify_token(refresh_data.refresh_token, expected_type="refresh")
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido")

    user_id = payload.get("sub")
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido")

    user = db.get(User, user_id_int)
    if user is None or not user.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo o no existe")

    context = get_user_security_context(db=db, user_id=user.id)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={
            "sub": str(user.id),
            "cedula": user.cedula,
            "store_id": context["store_id"],
            "is_superadmin": context["is_superadmin"],
        },
        expires_delta=access_token_expires,
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.get("/me", response_model=MeResponse)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Devuelve perfil y permisos efectivos del usuario autenticado."""
    context = get_user_security_context(db=db, user_id=current_user.id)
    return _build_auth_user(current_user, context)