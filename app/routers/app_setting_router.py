from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.app_setting_model import AppSetting
from app.schemas.app_setting_schema import AppSettingCreate, AppSettingRead
from config.config import get_db

router = APIRouter(prefix="/configuraciones-app", tags=["configuraciones-app"])


@router.get("", response_model=list[AppSettingRead])
def list_app_settings(db: Session = Depends(get_db)) -> list[AppSetting]:
    return db.query(AppSetting).order_by(AppSetting.id.asc()).all()


@router.post("", response_model=AppSettingRead, status_code=status.HTTP_201_CREATED)
def create_app_setting(payload: AppSettingCreate, db: Session = Depends(get_db)) -> AppSetting:
    row = AppSetting(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Clave de configuracion duplicada.")

    db.refresh(row)
    return row
