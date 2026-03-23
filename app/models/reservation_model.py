from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base
from app.models.enums import ReservaEstado


class Reservation(Base):
    __tablename__ = "reservas"
    __table_args__ = (
        CheckConstraint("fecha_hora_fin > fecha_hora_inicio", name="ck_reserva_fechas"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    mesa_id: Mapped[int] = mapped_column(ForeignKey("mesas.id", ondelete="RESTRICT"), nullable=False)
    nombre_cliente: Mapped[str] = mapped_column(String(120), nullable=False)
    fecha_hora_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fecha_hora_fin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[ReservaEstado] = mapped_column(
        Enum(ReservaEstado, name="reserva_estado"),
        nullable=False,
        default=ReservaEstado.ACTIVA,
        server_default=ReservaEstado.ACTIVA.value,
    )
    creado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
