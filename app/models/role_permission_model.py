from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class RolePermission(Base):
    __tablename__ = "rol_permiso"
    __table_args__ = (UniqueConstraint("rol_id", "permiso_id", name="uq_rol_permiso_rol_permiso"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permiso_id: Mapped[int] = mapped_column(ForeignKey("permisos.id", ondelete="CASCADE"), nullable=False)
