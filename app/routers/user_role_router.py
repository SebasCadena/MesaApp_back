from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_role_model import UserRole
from app.schemas.user_role_schema import UserRoleCreate, UserRoleRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/usuarios-roles", tags=["usuarios-roles"])


@router.get("", response_model=list[UserRoleRead])
def list_user_roles(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["usuarios_roles.ver"])),
) -> list[UserRole]:
    return db.query(UserRole).order_by(UserRole.id.asc()).all()


@router.post("", response_model=UserRoleRead, status_code=status.HTTP_201_CREATED)
def create_user_role(
    payload: UserRoleCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["usuarios_roles.crear"])),
) -> UserRole:
    row = UserRole(**payload.model_dump(exclude_none=True))
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Relacion usuario-rol invalida o duplicada.",
        )

    db.refresh(row)
    return row
