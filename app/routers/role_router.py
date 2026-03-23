from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.role_model import Role
from app.schemas.role_schema import RoleCreate, RoleRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleRead])
def list_roles(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["roles.ver"])),
) -> list[Role]:
    return db.query(Role).order_by(Role.id.asc()).all()


@router.post("", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["roles.crear"])),
) -> Role:
    role = Role(**payload.model_dump())
    db.add(role)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El rol ya existe.")

    db.refresh(role)
    return role
