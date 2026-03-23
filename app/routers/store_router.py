from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.store_model import Store
from app.schemas.store_schema import StoreCreate, StoreRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/tiendas", tags=["tiendas"])


@router.get("", response_model=list[StoreRead])
def list_stores(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["tiendas.ver"])),
) -> list[Store]:
    return db.query(Store).order_by(Store.id.asc()).all()


@router.post("", response_model=StoreRead, status_code=status.HTTP_201_CREATED)
def create_store(
    payload: StoreCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["tiendas.crear"])),
) -> Store:
    store = Store(**payload.model_dump())
    db.add(store)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una tienda con el mismo slug o NIT.",
        )

    db.refresh(store)
    return store
