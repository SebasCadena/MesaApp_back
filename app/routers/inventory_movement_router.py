from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.inventory_movement_model import InventoryMovement
from app.schemas.inventory_movement_schema import InventoryMovementCreate, InventoryMovementRead
from config.config import get_db

router = APIRouter(prefix="/movimientos-inventario", tags=["movimientos-inventario"])


@router.get("", response_model=list[InventoryMovementRead])
def list_inventory_movements(db: Session = Depends(get_db)) -> list[InventoryMovement]:
    return db.query(InventoryMovement).order_by(InventoryMovement.id.asc()).all()


@router.post("", response_model=InventoryMovementRead, status_code=status.HTTP_201_CREATED)
def create_inventory_movement(
    payload: InventoryMovementCreate, db: Session = Depends(get_db)
) -> InventoryMovement:
    row = InventoryMovement(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Movimiento invalido o con FK inexistente.",
        )

    db.refresh(row)
    return row
