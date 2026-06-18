from app.models.animal import Animal
from app.models.appointment_status_history import AppointmentStatusHistory
from app.models.consulta import Consulta
from app.models.enums import ConsultaStatus, Especialidade, Especie, TipoServico
from app.models.prescricao import Prescricao
from app.models.tutor import Tutor
from app.models.veterinario import Veterinario

__all__ = [
    "Animal",
    "AppointmentStatusHistory",
    "Consulta",
    "ConsultaStatus",
    "Especialidade",
    "Especie",
    "Prescricao",
    "TipoServico",
    "Tutor",
    "Veterinario",
]
