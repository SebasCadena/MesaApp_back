from datetime import date

from sqlalchemy import Boolean, CheckConstraint, Date, ForeignKey, Numeric, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class UserRole(Base):
    __tablename__ = "usuario_rol"
    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "rol_id",
            "tienda_id",
            "fecha_inicio",
            name="uq_usuario_rol_inicio",
        ),
        CheckConstraint("fecha_fin IS NULL OR fecha_fin >= fecha_inicio", name="ck_usuario_rol_fechas"),
        CheckConstraint("salario IS NULL OR salario >= 0", name="ck_usuario_rol_salario"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    salario: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    fecha_contrato: Mapped[date | None] = mapped_column(Date, nullable=True)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    fecha_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
