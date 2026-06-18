"""Migration 2: urgente, valor_total e constraint de datas."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_add_urgente_valor_total"
down_revision: Union[str, None] = "001_initial_structure"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "consultas",
        sa.Column("urgente", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "consultas",
        sa.Column("valor_total", sa.Numeric(precision=10, scale=2), nullable=True),
    )
    op.create_check_constraint(
        "ck_consultas_data_hora_fim_maior_inicio",
        "consultas",
        "data_hora_fim > data_hora_inicio",
    )


def downgrade() -> None:
    op.drop_constraint("ck_consultas_data_hora_fim_maior_inicio", "consultas", type_="check")
    op.drop_column("consultas", "valor_total")
    op.drop_column("consultas", "urgente")
