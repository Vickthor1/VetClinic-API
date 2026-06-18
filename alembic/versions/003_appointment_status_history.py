"""Migration 3: appointment_status_history."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "003_appointment_status_history"
down_revision: Union[str, None] = "002_add_urgente_valor_total"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

consulta_status_enum = postgresql.ENUM(
    "AGENDADO",
    "CONFIRMADO",
    "EM_ATENDIMENTO",
    "CONCLUIDO",
    "CANCELADO",
    "NAO_COMPARECEU",
    name="consulta_status_enum",
    create_type=False,
)


def upgrade() -> None:
    op.create_table(
        "appointment_status_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("old_status", consulta_status_enum, nullable=True),
        sa.Column("new_status", consulta_status_enum, nullable=False),
        sa.Column(
            "changed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("changed_by", sa.String(length=100), nullable=False, server_default="system"),
        sa.ForeignKeyConstraint(["appointment_id"], ["consultas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_appointment_status_history_appointment_id",
        "appointment_status_history",
        ["appointment_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_appointment_status_history_appointment_id",
        table_name="appointment_status_history",
    )
    op.drop_table("appointment_status_history")
