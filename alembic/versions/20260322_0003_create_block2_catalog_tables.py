"""create block 2 catalog tables

Revision ID: 20260322_0003
Revises: 20260322_0002
Create Date: 2026-03-22 01:15:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260322_0003"
down_revision: Union[str, Sequence[str], None] = "20260322_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tienda_id", "nombre", name="uq_categoria_tienda_nombre"),
    )

    op.create_table(
        "productos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("precio", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("categoria_id", sa.Integer(), nullable=False),
        sa.Column("img_url", sa.Text(), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("stock", sa.Numeric(precision=12, scale=3), server_default="0", nullable=False),
        sa.Column("stock_minimo", sa.Numeric(precision=12, scale=3), server_default="0", nullable=False),
        sa.Column("usa_receta", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("precio > 0", name="ck_producto_precio"),
        sa.CheckConstraint("stock >= 0", name="ck_producto_stock"),
        sa.CheckConstraint("stock_minimo >= 0", name="ck_producto_stock_minimo"),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tienda_id", "nombre", name="uq_producto_tienda_nombre"),
    )

    op.create_table(
        "materiales",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("unidad", sa.String(length=20), nullable=False),
        sa.Column("stock", sa.Numeric(precision=12, scale=3), server_default="0", nullable=False),
        sa.Column("stock_minimo", sa.Numeric(precision=12, scale=3), server_default="0", nullable=False),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("stock >= 0", name="ck_material_stock"),
        sa.CheckConstraint("stock_minimo >= 0", name="ck_material_stock_minimo"),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tienda_id", "nombre", name="uq_material_tienda_nombre"),
    )

    op.create_table(
        "producto_material",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("material_id", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.CheckConstraint("cantidad > 0", name="ck_producto_material_cantidad"),
        sa.ForeignKeyConstraint(["material_id"], ["materiales.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["producto_id"], ["productos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("producto_id", "material_id", name="uq_producto_material"),
    )


def downgrade() -> None:
    op.drop_table("producto_material")
    op.drop_table("materiales")
    op.drop_table("productos")
    op.drop_table("categorias")
