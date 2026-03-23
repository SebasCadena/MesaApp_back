"""create block 4 support tables

Revision ID: 20260322_0005
Revises: 20260322_0004
Create Date: 2026-03-22 02:20:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260322_0005"
down_revision: Union[str, Sequence[str], None] = "20260322_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    tipo_movimiento_inventario = postgresql.ENUM(
        "ENTRADA",
        "SALIDA",
        "AJUSTE",
        name="tipo_movimiento_inventario",
        create_type=False,
    )

    bind = op.get_bind()
    tipo_movimiento_inventario.create(bind, checkfirst=True)

    op.create_table(
        "configuraciones_app",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("clave", sa.String(length=100), nullable=False),
        sa.Column("valor", sa.Text(), nullable=True),
        sa.Column("tipo_valor", sa.String(length=20), server_default="string", nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("editable", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("actualizado_por_usuario_id", sa.Integer(), nullable=True),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["actualizado_por_usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("clave"),
    )
    op.create_index("ix_configuraciones_app_clave", "configuraciones_app", ["clave"], unique=True)

    op.create_table(
        "configuraciones_tienda",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("clave", sa.String(length=100), nullable=False),
        sa.Column("valor", sa.Text(), nullable=True),
        sa.Column("tipo_valor", sa.String(length=20), server_default="string", nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("editable", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("actualizado_por_usuario_id", sa.Integer(), nullable=True),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["actualizado_por_usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tienda_id", "clave", name="uq_config_tienda_clave"),
    )

    op.create_table(
        "movimientos_inventario",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("material_id", sa.Integer(), nullable=True),
        sa.Column("producto_id", sa.Integer(), nullable=True),
        sa.Column("tipo_movimiento", tipo_movimiento_inventario, nullable=False),
        sa.Column("cantidad", sa.Numeric(12, 3), nullable=False),
        sa.Column("motivo", sa.String(length=255), nullable=True),
        sa.Column("creado_por_usuario_id", sa.Integer(), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("cantidad > 0", name="ck_mov_inv_cantidad"),
        sa.CheckConstraint(
            "material_id IS NOT NULL OR producto_id IS NOT NULL",
            name="ck_mov_inv_material_o_producto",
        ),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["material_id"], ["materiales.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["producto_id"], ["productos.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["creado_por_usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("movimientos_inventario")
    op.drop_table("configuraciones_tienda")
    op.drop_index("ix_configuraciones_app_clave", table_name="configuraciones_app")
    op.drop_table("configuraciones_app")

    bind = op.get_bind()
    postgresql.ENUM(name="tipo_movimiento_inventario").drop(bind, checkfirst=True)
