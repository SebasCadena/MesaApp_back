from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class AppSetting(Base):
    __tablename__ = "configuraciones_app"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    clave: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
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
