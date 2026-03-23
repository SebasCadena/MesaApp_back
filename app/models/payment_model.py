from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base
from app.models.enums import MetodoPago


class Payment(Base):
    __tablename__ = "pagos"
    __table_args__ = (CheckConstraint("monto > 0", name="ck_pago_monto"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    monto: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    metodo_pago: Mapped[MetodoPago] = mapped_column(Enum(MetodoPago, name="metodo_pago"), nullable=False)
    referencia_externa: Mapped[str | None] = mapped_column(String(120), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    creado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
