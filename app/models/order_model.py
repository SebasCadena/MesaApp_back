from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base
from app.models.enums import PedidoEstado, PedidoTipo


class Order(Base):
    __tablename__ = "pedidos"
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="ck_pedido_subtotal"),
        CheckConstraint("impuesto >= 0", name="ck_pedido_impuesto"),
        CheckConstraint("descuento >= 0", name="ck_pedido_descuento"),
        CheckConstraint("total >= 0", name="ck_pedido_total"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    mesa_id: Mapped[int | None] = mapped_column(ForeignKey("mesas.id", ondelete="SET NULL"), nullable=True)
    tipo: Mapped[PedidoTipo] = mapped_column(Enum(PedidoTipo, name="pedido_tipo"), nullable=False)
    estado: Mapped[PedidoEstado] = mapped_column(
        Enum(PedidoEstado, name="pedido_estado"),
        nullable=False,
        default=PedidoEstado.PENDIENTE,
        server_default=PedidoEstado.PENDIENTE.value,
    )
    subtotal: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0, server_default="0")
    impuesto: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0, server_default="0")
    descuento: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0, server_default="0")
    total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0, server_default="0")
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    creado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
