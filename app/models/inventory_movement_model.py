from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base
from app.models.enums import TipoMovimientoInventario


class InventoryMovement(Base):
    __tablename__ = "movimientos_inventario"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_mov_inv_cantidad"),
        CheckConstraint(
            "material_id IS NOT NULL OR producto_id IS NOT NULL",
            name="ck_mov_inv_material_o_producto",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    material_id: Mapped[int | None] = mapped_column(
        ForeignKey("materiales.id", ondelete="SET NULL"), nullable=True
    )
    producto_id: Mapped[int | None] = mapped_column(
        ForeignKey("productos.id", ondelete="SET NULL"), nullable=True
    )
    tipo_movimiento: Mapped[TipoMovimientoInventario] = mapped_column(
        Enum(TipoMovimientoInventario, name="tipo_movimiento_inventario"), nullable=False
    )
    cantidad: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    motivo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    creado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
