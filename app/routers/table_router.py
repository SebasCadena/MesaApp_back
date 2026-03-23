from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.table_model import TableModel
from app.schemas.table_schema import TableCreate, TableRead
from config.config import get_db

router = APIRouter(prefix="/mesas", tags=["mesas"])


@router.get("", response_model=list[TableRead])
def list_tables(db: Session = Depends(get_db)) -> list[TableModel]:
    return db.query(TableModel).order_by(TableModel.id.asc()).all()


@router.post("", response_model=TableRead, status_code=status.HTTP_201_CREATED)
def create_table(payload: TableCreate, db: Session = Depends(get_db)) -> TableModel:
    row = TableModel(**payload.model_dump())
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mesa invalida o duplicada.")

    db.refresh(row)
    return row
