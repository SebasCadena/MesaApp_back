from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.order_detail_model import OrderDetail
from app.schemas.order_detail_schema import OrderDetailCreate, OrderDetailRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/detalles-pedido", tags=["detalles-pedido"])


@router.get("", response_model=list[OrderDetailRead])
def list_order_details(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["detalle_pedido.ver"])),
) -> list[OrderDetail]:
    return db.query(OrderDetail).order_by(OrderDetail.id.asc()).all()


@router.post("", response_model=OrderDetailRead, status_code=status.HTTP_201_CREATED)
def create_order_detail(
    payload: OrderDetailCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["detalle_pedido.crear"])),
) -> OrderDetail:
    row = OrderDetail(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Detalle invalido, duplicado o con FK inexistente.",
        )

    db.refresh(row)
    return row
