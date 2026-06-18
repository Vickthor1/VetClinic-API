from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ConsultaStatus


class AppointmentStatusHistory(Base):
    __tablename__ = "appointment_status_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("consultas.id"), nullable=False, index=True
    )
    old_status: Mapped[ConsultaStatus | None] = mapped_column(
        Enum(ConsultaStatus, name="consulta_status_enum", create_type=False, native_enum=False),
        nullable=True,
    )
    new_status: Mapped[ConsultaStatus] = mapped_column(
        Enum(ConsultaStatus, name="consulta_status_enum", create_type=False, native_enum=False),
        nullable=False,
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    changed_by: Mapped[str] = mapped_column(String(100), nullable=False, default="system")

    appointment: Mapped["Consulta"] = relationship(back_populates="status_history")
