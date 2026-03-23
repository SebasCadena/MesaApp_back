"""create block 1 security tables

Revision ID: 20260322_0002
Revises: 20260322_0001
Create Date: 2026-03-22 00:30:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260322_0002"
down_revision: Union[str, Sequence[str], None] = "20260322_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("cedula", sa.String(length=30), nullable=False),
        sa.Column("celular", sa.String(length=30), nullable=True),
        sa.Column("correo", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("direccion", sa.String(length=255), nullable=True),
        sa.Column("fecha_nacimiento", sa.Date(), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cedula"),
        sa.UniqueConstraint("celular"),
        sa.UniqueConstraint("correo"),
    )
    op.create_index("ix_usuarios_cedula", "usuarios", ["cedula"], unique=True)
    op.create_index("ix_usuarios_correo", "usuarios", ["correo"], unique=True)

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index("ix_roles_nombre", "roles", ["nombre"], unique=True)

    op.create_table(
        "permisos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index("ix_permisos_nombre", "permisos", ["nombre"], unique=True)

    op.create_table(
        "rol_permiso",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("rol_id", sa.Integer(), nullable=False),
        sa.Column("permiso_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["rol_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["permiso_id"], ["permisos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rol_id", "permiso_id", name="uq_rol_permiso_rol_permiso"),
    )

    op.create_table(
        "usuario_rol",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("rol_id", sa.Integer(), nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("salario", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("fecha_contrato", sa.Date(), nullable=True),
        sa.Column("fecha_inicio", sa.Date(), server_default=sa.text("CURRENT_DATE"), nullable=False),
        sa.Column("fecha_fin", sa.Date(), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.CheckConstraint("fecha_fin IS NULL OR fecha_fin >= fecha_inicio", name="ck_usuario_rol_fechas"),
        sa.CheckConstraint("salario IS NULL OR salario >= 0", name="ck_usuario_rol_salario"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["rol_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("usuario_id", "rol_id", "tienda_id", "fecha_inicio", name="uq_usuario_rol_inicio"),
    )


def downgrade() -> None:
    op.drop_table("usuario_rol")
    op.drop_table("rol_permiso")

    op.drop_index("ix_permisos_nombre", table_name="permisos")
    op.drop_table("permisos")

    op.drop_index("ix_roles_nombre", table_name="roles")
    op.drop_table("roles")

    op.drop_index("ix_usuarios_correo", table_name="usuarios")
    op.drop_index("ix_usuarios_cedula", table_name="usuarios")
    op.drop_table("usuarios")
