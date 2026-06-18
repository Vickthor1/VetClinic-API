from sqlalchemy.orm import Session

from app.models.appointment_status_history import AppointmentStatusHistory
from app.models.enums import ConsultaStatus


class AppointmentStatusHistoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        appointment_id: int,
        old_status: ConsultaStatus | None,
        new_status: ConsultaStatus,
        changed_by: str = "system",
    ) -> AppointmentStatusHistory:
        history = AppointmentStatusHistory(
            appointment_id=appointment_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
        )
        self.db.add(history)
        self.db.flush()
        self.db.refresh(history)
        return history

    def get_by_appointment_id(self, appointment_id: int) -> list[AppointmentStatusHistory]:
        return (
            self.db.query(AppointmentStatusHistory)
            .filter(AppointmentStatusHistory.appointment_id == appointment_id)
            .order_by(AppointmentStatusHistory.changed_at.asc())
            .all()
        )
