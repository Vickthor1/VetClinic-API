from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import Especie


class Animal(Base):
    __tablename__ = "animais"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutores.id"), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    especie: Mapped[Especie] = mapped_column(
        Enum(Especie, name="especie_enum", native_enum=False), nullable=False
    )
    raca: Mapped[str] = mapped_column(String(100), nullable=False)
    peso_kg: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    obito: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    data_obito: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    tutor: Mapped["Tutor"] = relationship(back_populates="animais")
    consultas: Mapped[list["Consulta"]] = relationship(back_populates="animal")
