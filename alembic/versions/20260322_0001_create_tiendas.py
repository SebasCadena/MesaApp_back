"""create tiendas table

Revision ID: 20260322_0001
Revises:
Create Date: 2026-03-22 00:00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260322_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tiendas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("nit", sa.String(length=40), nullable=True),
        sa.Column("telefono", sa.String(length=30), nullable=True),
        sa.Column("correo", sa.String(length=120), nullable=True),
        sa.Column("direccion", sa.String(length=255), nullable=True),
        sa.Column("ciudad", sa.String(length=80), nullable=True),
        sa.Column("pais", sa.String(length=80), server_default="CO", nullable=False),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("nit"),
    )
    op.create_index("ix_tiendas_slug", "tiendas", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_tiendas_slug", table_name="tiendas")
    op.drop_table("tiendas")
