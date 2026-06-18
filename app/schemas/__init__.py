from app.schemas.animal import AnimalCreate, AnimalResponse, AnimalUpdate
from app.schemas.appointment_status_history import AppointmentStatusHistoryResponse
from app.schemas.consulta import (
    ConsultaCancel,
    ConsultaCreate,
    ConsultaListResponse,
    ConsultaResponse,
    ConsultaUpdate,
)
from app.schemas.prescricao import PrescricaoCreate, PrescricaoResponse, PrescricaoUpdate
from app.schemas.tutor import TutorCreate, TutorResponse, TutorUpdate
from app.schemas.veterinario import (
    VeterinarioCreate,
    VeterinarioResponse,
    VeterinarioUpdate,
)

__all__ = [
    "AnimalCreate",
    "AnimalResponse",
    "AnimalUpdate",
    "AppointmentStatusHistoryResponse",
    "ConsultaCancel",
    "ConsultaCreate",
    "ConsultaListResponse",
    "ConsultaResponse",
    "ConsultaUpdate",
    "PrescricaoCreate",
    "PrescricaoResponse",
    "PrescricaoUpdate",
    "TutorCreate",
    "TutorResponse",
    "TutorUpdate",
    "VeterinarioCreate",
    "VeterinarioResponse",
    "VeterinarioUpdate",
]
