from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class Product(Base):
    __tablename__ = "productos"
    __table_args__ = (
        UniqueConstraint("tienda_id", "nombre", name="uq_producto_tienda_nombre"),
        CheckConstraint("precio > 0", name="ck_producto_precio"),
        CheckConstraint("stock >= 0", name="ck_producto_stock"),
        CheckConstraint("stock_minimo >= 0", name="ck_producto_stock_minimo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False)
    img_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    stock: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0, server_default="0")
    stock_minimo: Mapped[float] = mapped_column(
        Numeric(12, 3), nullable=False, default=0, server_default="0"
    )
    usa_receta: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
