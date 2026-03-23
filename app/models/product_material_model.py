from sqlalchemy import CheckConstraint, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class ProductMaterial(Base):
    __tablename__ = "producto_material"
    __table_args__ = (
        UniqueConstraint("producto_id", "material_id", name="uq_producto_material"),
        CheckConstraint("cantidad > 0", name="ck_producto_material_cantidad"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id", ondelete="CASCADE"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materiales.id", ondelete="CASCADE"), nullable=False)
    cantidad: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
