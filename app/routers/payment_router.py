from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.payment_model import Payment
from app.schemas.payment_schema import PaymentCreate, PaymentRead
from config.config import get_db

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("", response_model=list[PaymentRead])
def list_payments(db: Session = Depends(get_db)) -> list[Payment]:
    return db.query(Payment).order_by(Payment.id.asc()).all()


@router.post("", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)) -> Payment:
    row = Payment(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pago invalido, duplicado o con FK inexistente.",
        )

    db.refresh(row)
    return row
