from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("", response_model=list[ProductRead])
def list_products(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["productos.ver"])),
) -> list[Product]:
    return db.query(Product).order_by(Product.id.asc()).all()


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["productos.crear"])),
) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Producto invalido, duplicado o con FK inexistente.",
        )

    db.refresh(product)
    return product
