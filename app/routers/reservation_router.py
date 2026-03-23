from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.reservation_model import Reservation
from app.schemas.reservation_schema import ReservationCreate, ReservationRead
from auth.roles import require_permissions
from config.config import get_db

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.get("", response_model=list[ReservationRead])
def list_reservations(
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["reservas.ver"])),
) -> list[Reservation]:
    return db.query(Reservation).order_by(Reservation.id.asc()).all()


@router.post("", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(
    payload: ReservationCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_permissions(["reservas.crear"])),
) -> Reservation:
    row = Reservation(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reserva invalida, duplicada o con FK inexistente.",
        )

    db.refresh(row)
    return row
