from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Configuración de seguridad
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY no configurada")

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Para encriptar contraseñas - usando argon2 en lugar de bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Convierte una contraseña en texto plano a hash"""
    return pwd_context.hash(password)

def _create_token(data: dict[str, Any], expires_delta: timedelta, token_type: str) -> str:
    """Crea un token JWT de tipo access o refresh."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    to_encode.update({"exp": expire, "iat": now, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Crea un access token JWT."""
    token_ttl = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(data=data, expires_delta=token_ttl, token_type="access")

def create_refresh_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Crea un refresh token JWT."""
    token_ttl = expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(data=data, expires_delta=token_ttl, token_type="refresh")

def verify_token(token: str, expected_type: str | None = None) -> dict[str, Any] | None:
    """Verifica que el token sea válido y devuelve sus claims."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if expected_type and payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None