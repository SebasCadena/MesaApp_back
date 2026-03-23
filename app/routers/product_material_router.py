from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product_material_model import ProductMaterial
from app.schemas.product_material_schema import ProductMaterialCreate, ProductMaterialRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/productos-materiales", tags=["productos-materiales"])


@router.get("", response_model=list[ProductMaterialRead])
def list_product_materials(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["productos_materiales.ver"])),
) -> list[ProductMaterial]:
    return db.query(ProductMaterial).order_by(ProductMaterial.id.asc()).all()


@router.post("", response_model=ProductMaterialRead, status_code=status.HTTP_201_CREATED)
def create_product_material(
    payload: ProductMaterialCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["productos_materiales.crear"])),
) -> ProductMaterial:
    row = ProductMaterial(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Relacion producto-material invalida o duplicada.",
        )

    db.refresh(row)
    return row
