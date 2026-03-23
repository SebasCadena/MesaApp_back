from sqlalchemy import CheckConstraint, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class OrderDetail(Base):
    __tablename__ = "detalle_pedido"
    __table_args__ = (
        UniqueConstraint("pedido_id", "producto_id", name="uq_detalle_pedido_producto"),
        CheckConstraint("cantidad > 0", name="ck_detalle_cantidad"),
        CheckConstraint("precio_unitario >= 0", name="ck_detalle_precio_unitario"),
        CheckConstraint("subtotal_linea >= 0", name="ck_detalle_subtotal_linea"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id", ondelete="RESTRICT"), nullable=False)
    cantidad: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    subtotal_linea: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
