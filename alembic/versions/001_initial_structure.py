"""Migration 1: estrutura inicial."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial_structure"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

especie_enum = postgresql.ENUM(
    "CACHORRO", "GATO", "AVE", "REPTIL", "OUTRO", name="especie_enum", create_type=False
)
tipo_servico_enum = postgresql.ENUM(
    "CONSULTA",
    "RETORNO",
    "CIRURGIA",
    "EXAME",
    "VACINA",
    name="tipo_servico_enum",
    create_type=False,
)
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
    op.execute(
        "CREATE TYPE especie_enum AS ENUM ('CACHORRO', 'GATO', 'AVE', 'REPTIL', 'OUTRO')"
    )
    op.execute(
        "CREATE TYPE tipo_servico_enum AS ENUM "
        "('CONSULTA', 'RETORNO', 'CIRURGIA', 'EXAME', 'VACINA')"
    )
    op.execute(
        "CREATE TYPE consulta_status_enum AS ENUM "
        "('AGENDADO', 'CONFIRMADO', 'EM_ATENDIMENTO', 'CONCLUIDO', 'CANCELADO', 'NAO_COMPARECEU')"
    )

    op.create_table(
        "tutores",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cpf"),
    )
    op.create_index("ix_tutores_cpf", "tutores", ["cpf"], unique=False)

    op.create_table(
        "veterinarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("crmv", sa.String(length=20), nullable=False),
        sa.Column(
            "especialidades",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("crmv"),
    )
    op.create_index("ix_veterinarios_crmv", "veterinarios", ["crmv"], unique=False)

    op.create_table(
        "animais",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tutor_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("especie", especie_enum, nullable=False),
        sa.Column("raca", sa.String(length=100), nullable=False),
        sa.Column("peso_kg", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("data_nascimento", sa.Date(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("obito", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("data_obito", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["tutor_id"], ["tutores.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_animais_tutor_id", "animais", ["tutor_id"], unique=False)

    op.create_table(
        "consultas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("animal_id", sa.Integer(), nullable=False),
        sa.Column("veterinario_id", sa.Integer(), nullable=False),
        sa.Column("tipo_servico", tipo_servico_enum, nullable=False),
        sa.Column(
            "status",
            consulta_status_enum,
            nullable=False,
            server_default=sa.text("'AGENDADO'::consulta_status_enum"),
        ),
        sa.Column("data_hora_inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_hora_fim", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valor_base", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("motivo_cancelamento", sa.Text(), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["animal_id"], ["animais.id"]),
        sa.ForeignKeyConstraint(["veterinario_id"], ["veterinarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_consultas_animal_id", "consultas", ["animal_id"], unique=False)
    op.create_index(
        "ix_consultas_veterinario_id", "consultas", ["veterinario_id"], unique=False
    )

    op.create_table(
        "prescricoes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("consulta_id", sa.Integer(), nullable=False),
        sa.Column("medicamento", sa.String(length=255), nullable=False),
        sa.Column("dosagem", sa.String(length=100), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("frequencia", sa.String(length=100), nullable=False),
        sa.Column("duracao_dias", sa.Integer(), nullable=False),
        sa.Column("valor_unitario", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["consulta_id"], ["consultas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_prescricoes_consulta_id", "prescricoes", ["consulta_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_prescricoes_consulta_id", table_name="prescricoes")
    op.drop_table("prescricoes")
    op.drop_index("ix_consultas_veterinario_id", table_name="consultas")
    op.drop_index("ix_consultas_animal_id", table_name="consultas")
    op.drop_table("consultas")
    op.drop_index("ix_animais_tutor_id", table_name="animais")
    op.drop_table("animais")
    op.drop_index("ix_veterinarios_crmv", table_name="veterinarios")
    op.drop_table("veterinarios")
    op.drop_index("ix_tutores_cpf", table_name="tutores")
    op.drop_table("tutores")

    op.execute("DROP TYPE IF EXISTS consulta_status_enum")
    op.execute("DROP TYPE IF EXISTS tipo_servico_enum")
    op.execute("DROP TYPE IF EXISTS especie_enum")
