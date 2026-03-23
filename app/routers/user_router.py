from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserRead
from auth.auth import get_password_hash
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["usuarios.ver"])),
) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["usuarios.crear"])),
) -> User:
    data = payload.model_dump()
    data["password_hash"] = get_password_hash(data["password_hash"])
    user = User(**data)
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con cedula, correo o celular duplicado.",
        )

    db.refresh(user)
    return user
