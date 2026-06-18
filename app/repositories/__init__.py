from app.repositories.animal_repository import AnimalRepository
from app.repositories.appointment_status_history_repository import (
    AppointmentStatusHistoryRepository,
)
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.prescricao_repository import PrescricaoRepository
from app.repositories.tutor_repository import TutorRepository
from app.repositories.veterinario_repository import VeterinarioRepository

__all__ = [
    "AnimalRepository",
    "AppointmentStatusHistoryRepository",
    "ConsultaRepository",
    "PrescricaoRepository",
    "TutorRepository",
    "VeterinarioRepository",
]
