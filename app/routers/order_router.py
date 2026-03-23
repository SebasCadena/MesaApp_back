from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate, OrderRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("", response_model=list[OrderRead])
def list_orders(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["pedidos.ver"])),
) -> list[Order]:
    return db.query(Order).order_by(Order.id.asc()).all()


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["pedidos.crear"])),
) -> Order:
    row = Order(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pedido invalido, duplicado o con FK inexistente.",
        )

    db.refresh(row)
    return row
