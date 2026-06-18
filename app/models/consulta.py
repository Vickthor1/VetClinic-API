from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ConsultaStatus, TipoServico


class Consulta(Base):
    __tablename__ = "consultas"
    __table_args__ = (
        CheckConstraint(
            "data_hora_fim > data_hora_inicio",
            name="ck_consultas_data_hora_fim_maior_inicio",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    animal_id: Mapped[int] = mapped_column(ForeignKey("animais.id"), nullable=False, index=True)
    veterinario_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarios.id"), nullable=False, index=True
    )
    tipo_servico: Mapped[TipoServico] = mapped_column(
        Enum(TipoServico, name="tipo_servico_enum", native_enum=False), nullable=False
    )
    status: Mapped[ConsultaStatus] = mapped_column(
        Enum(ConsultaStatus, name="consulta_status_enum", native_enum=False),
        nullable=False,
        default=ConsultaStatus.AGENDADO,
    )
    data_hora_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_hora_fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    urgente: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    valor_base: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valor_total: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    motivo_cancelamento: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    animal: Mapped["Animal"] = relationship(back_populates="consultas")
    veterinario: Mapped["Veterinario"] = relationship(back_populates="consultas")
    prescricoes: Mapped[list["Prescricao"]] = relationship(back_populates="consulta")
    status_history: Mapped[list["AppointmentStatusHistory"]] = relationship(
        back_populates="appointment"
    )
