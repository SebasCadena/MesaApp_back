from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base
from app.models.enums import MesaEstado


class TableModel(Base):
    __tablename__ = "mesas"
    __table_args__ = (
        UniqueConstraint("tienda_id", "numero", name="uq_mesa_tienda_numero"),
        CheckConstraint("capacidad_minima > 0", name="ck_mesa_capacidad_minima"),
        CheckConstraint("capacidad_maxima >= capacidad_minima", name="ck_mesa_capacidad_maxima"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    capacidad_minima: Mapped[int] = mapped_column(Integer, nullable=False)
    capacidad_maxima: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[MesaEstado] = mapped_column(
        Enum(MesaEstado, name="mesa_estado"),
        nullable=False,
        default=MesaEstado.DISPONIBLE,
        server_default=MesaEstado.DISPONIBLE.value,
    )
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
