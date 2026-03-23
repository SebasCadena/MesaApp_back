from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class Material(Base):
    __tablename__ = "materiales"
    __table_args__ = (
        UniqueConstraint("tienda_id", "nombre", name="uq_material_tienda_nombre"),
        CheckConstraint("stock >= 0", name="ck_material_stock"),
        CheckConstraint("stock_minimo >= 0", name="ck_material_stock_minimo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    unidad: Mapped[str] = mapped_column(String(20), nullable=False)
    stock: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0, server_default="0")
    stock_minimo: Mapped[float] = mapped_column(
        Numeric(12, 3), nullable=False, default=0, server_default="0"
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
