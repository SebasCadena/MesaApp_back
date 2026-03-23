"""create block 3 operation tables

Revision ID: 20260322_0004
Revises: 20260322_0003
Create Date: 2026-03-22 01:45:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260322_0004"
down_revision: Union[str, Sequence[str], None] = "20260322_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    mesa_estado = postgresql.ENUM(
        "DISPONIBLE",
        "OCUPADA",
        "RESERVADA",
        "MANTENIMIENTO",
        name="mesa_estado",
        create_type=False,
    )
    reserva_estado = postgresql.ENUM(
        "ACTIVA", "CANCELADA", "FINALIZADA", name="reserva_estado", create_type=False
    )
    pedido_estado = postgresql.ENUM(
        "PENDIENTE",
        "EN_PREPARACION",
        "LISTO",
        "ENTREGADO",
        "PAGADO",
        "CANCELADO",
        name="pedido_estado",
        create_type=False,
    )
    pedido_tipo = postgresql.ENUM("MESA", "DOMICILIO", name="pedido_tipo", create_type=False)
    metodo_pago = postgresql.ENUM(
        "EFECTIVO", "TARJETA", "TRANSFERENCIA", "QR", name="metodo_pago", create_type=False
    )

    bind = op.get_bind()
    mesa_estado.create(bind, checkfirst=True)
    reserva_estado.create(bind, checkfirst=True)
    pedido_estado.create(bind, checkfirst=True)
    pedido_tipo.create(bind, checkfirst=True)
    metodo_pago.create(bind, checkfirst=True)

    op.create_table(
        "mesas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("capacidad_minima", sa.Integer(), nullable=False),
        sa.Column("capacidad_maxima", sa.Integer(), nullable=False),
        sa.Column("estado", mesa_estado, server_default="DISPONIBLE", nullable=False),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("capacidad_minima > 0", name="ck_mesa_capacidad_minima"),
        sa.CheckConstraint("capacidad_maxima >= capacidad_minima", name="ck_mesa_capacidad_maxima"),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tienda_id", "numero", name="uq_mesa_tienda_numero"),
    )

    op.create_table(
        "reservas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("mesa_id", sa.Integer(), nullable=False),
        sa.Column("nombre_cliente", sa.String(length=120), nullable=False),
        sa.Column("fecha_hora_inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fecha_hora_fin", sa.DateTime(timezone=True), nullable=False),
        sa.Column("estado", reserva_estado, server_default="ACTIVA", nullable=False),
        sa.Column("creado_por_usuario_id", sa.Integer(), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("fecha_hora_fin > fecha_hora_inicio", name="ck_reserva_fechas"),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mesa_id"], ["mesas.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["creado_por_usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("mesa_id", sa.Integer(), nullable=True),
        sa.Column("tipo", pedido_tipo, nullable=False),
        sa.Column("estado", pedido_estado, server_default="PENDIENTE", nullable=False),
        sa.Column("subtotal", sa.Numeric(12, 2), server_default="0", nullable=False),
        sa.Column("impuesto", sa.Numeric(12, 2), server_default="0", nullable=False),
        sa.Column("descuento", sa.Numeric(12, 2), server_default="0", nullable=False),
        sa.Column("total", sa.Numeric(12, 2), server_default="0", nullable=False),
        sa.Column("notas", sa.Text(), nullable=True),
        sa.Column("creado_por_usuario_id", sa.Integer(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("subtotal >= 0", name="ck_pedido_subtotal"),
        sa.CheckConstraint("impuesto >= 0", name="ck_pedido_impuesto"),
        sa.CheckConstraint("descuento >= 0", name="ck_pedido_descuento"),
        sa.CheckConstraint("total >= 0", name="ck_pedido_total"),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mesa_id"], ["mesas.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["creado_por_usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "detalle_pedido",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Numeric(12, 3), nullable=False),
        sa.Column("precio_unitario", sa.Numeric(12, 2), nullable=False),
        sa.Column("subtotal_linea", sa.Numeric(12, 2), nullable=False),
        sa.CheckConstraint("cantidad > 0", name="ck_detalle_cantidad"),
        sa.CheckConstraint("precio_unitario >= 0", name="ck_detalle_precio_unitario"),
        sa.CheckConstraint("subtotal_linea >= 0", name="ck_detalle_subtotal_linea"),
        sa.ForeignKeyConstraint(["pedido_id"], ["pedidos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["producto_id"], ["productos.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pedido_id", "producto_id", name="uq_detalle_pedido_producto"),
    )

    op.create_table(
        "pagos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tienda_id", sa.Integer(), nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("monto", sa.Numeric(12, 2), nullable=False),
        sa.Column("metodo_pago", metodo_pago, nullable=False),
        sa.Column("referencia_externa", sa.String(length=120), nullable=True),
        sa.Column("fecha", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("creado_por_usuario_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("monto > 0", name="ck_pago_monto"),
        sa.ForeignKeyConstraint(["tienda_id"], ["tiendas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pedido_id"], ["pedidos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["creado_por_usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("pagos")
    op.drop_table("detalle_pedido")
    op.drop_table("pedidos")
    op.drop_table("reservas")
    op.drop_table("mesas")

    bind = op.get_bind()
    postgresql.ENUM(name="metodo_pago").drop(bind, checkfirst=True)
    postgresql.ENUM(name="pedido_tipo").drop(bind, checkfirst=True)
    postgresql.ENUM(name="pedido_estado").drop(bind, checkfirst=True)
    postgresql.ENUM(name="reserva_estado").drop(bind, checkfirst=True)
    postgresql.ENUM(name="mesa_estado").drop(bind, checkfirst=True)
