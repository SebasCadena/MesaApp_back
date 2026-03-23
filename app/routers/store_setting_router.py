from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.store_setting_model import StoreSetting
from app.schemas.store_setting_schema import StoreSettingCreate, StoreSettingRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/configuraciones-tienda", tags=["configuraciones-tienda"])


@router.get("", response_model=list[StoreSettingRead])
def list_store_settings(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["config_tienda.ver"])),
) -> list[StoreSetting]:
    return db.query(StoreSetting).order_by(StoreSetting.id.asc()).all()


@router.post("", response_model=StoreSettingRead, status_code=status.HTTP_201_CREATED)
def create_store_setting(
    payload: StoreSettingCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["config_tienda.crear"])),
) -> StoreSetting:
    row = StoreSetting(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Configuracion duplicada o tienda/usuario invalido.",
        )

    db.refresh(row)
    return row
