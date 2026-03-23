from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.permission_model import Permission
from app.schemas.permission_schema import PermissionCreate, PermissionRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/permisos", tags=["permisos"])


@router.get("", response_model=list[PermissionRead])
def list_permissions(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["permisos.ver"])),
) -> list[Permission]:
    return db.query(Permission).order_by(Permission.id.asc()).all()


@router.post("", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["permisos.crear"])),
) -> Permission:
    permission = Permission(**payload.model_dump())
    db.add(permission)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El permiso ya existe.")

    db.refresh(permission)
    return permission
