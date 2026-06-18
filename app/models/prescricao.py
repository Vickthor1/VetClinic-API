from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Prescricao(Base):
    __tablename__ = "prescricoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    consulta_id: Mapped[int] = mapped_column(
        ForeignKey("consultas.id"), nullable=False, index=True
    )
    medicamento: Mapped[str] = mapped_column(String(255), nullable=False)
    dosagem: Mapped[str] = mapped_column(String(100), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    frequencia: Mapped[str] = mapped_column(String(100), nullable=False)
    duracao_dias: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    consulta: Mapped["Consulta"] = relationship(back_populates="prescricoes")
