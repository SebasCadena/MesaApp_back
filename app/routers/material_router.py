from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.material_model import Material
from app.schemas.material_schema import MaterialCreate, MaterialRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/materiales", tags=["materiales"])


@router.get("", response_model=list[MaterialRead])
def list_materials(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["materiales.ver"])),
) -> list[Material]:
    return db.query(Material).order_by(Material.id.asc()).all()


@router.post("", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
def create_material(
    payload: MaterialCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["materiales.crear"])),
) -> Material:
    material = Material(**payload.model_dump())
    db.add(material)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Material duplicado o tienda invalida.",
        )

    db.refresh(material)
    return material
