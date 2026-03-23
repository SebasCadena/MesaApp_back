from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.role_permission_model import RolePermission
from app.schemas.role_permission_schema import RolePermissionCreate, RolePermissionRead
from config.config import get_db

router = APIRouter(prefix="/roles-permisos", tags=["roles-permisos"])


@router.get("", response_model=list[RolePermissionRead])
def list_role_permissions(db: Session = Depends(get_db)) -> list[RolePermission]:
    return db.query(RolePermission).order_by(RolePermission.id.asc()).all()


@router.post("", response_model=RolePermissionRead, status_code=status.HTTP_201_CREATED)
def create_role_permission(payload: RolePermissionCreate, db: Session = Depends(get_db)) -> RolePermission:
    row = RolePermission(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Relacion rol-permiso invalida o duplicada.",
        )

    db.refresh(row)
    return row
