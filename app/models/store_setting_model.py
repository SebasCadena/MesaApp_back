from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class StoreSetting(Base):
    __tablename__ = "configuraciones_tienda"
    __table_args__ = (UniqueConstraint("tienda_id", "clave", name="uq_config_tienda_clave"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tienda_id: Mapped[int] = mapped_column(ForeignKey("tiendas.id", ondelete="CASCADE"), nullable=False)
    clave: Mapped[str] = mapped_column(String(100), nullable=False)
    valor: Mapped[str | None] = mapped_column(Text, nullable=True)
    tipo_valor: Mapped[str] = mapped_column(
        String(20), nullable=False, default="string", server_default="string"
    )
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    editable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    actualizado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
