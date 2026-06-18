from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ConsultaStatus


class AppointmentStatusHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    old_status: ConsultaStatus | None
    new_status: ConsultaStatus
    changed_at: datetime
    changed_by: str
