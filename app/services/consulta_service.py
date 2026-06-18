from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import (
    AppointmentNotInProgressException,
    CancellationReasonRequiredException,
    InvalidTransitionException,
    NotFoundException,
    OwnerInactiveException,
    PetDeceasedException,
    ScheduleConflictException,
    VetInactiveException,
    VetMissingSpecialtyException,
)
from app.models.enums import ConsultaStatus, Especialidade, TipoServico
from app.repositories.animal_repository import AnimalRepository
from app.repositories.appointment_status_history_repository import (
    AppointmentStatusHistoryRepository,
)
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.prescricao_repository import PrescricaoRepository
from app.repositories.tutor_repository import TutorRepository
from app.repositories.veterinario_repository import VeterinarioRepository
from app.schemas.consulta import (
    ConsultaCancel,
    ConsultaCreate,
    ConsultaListResponse,
    ConsultaResponse,
    ConsultaUpdate,
)

VALID_TRANSITIONS: dict[ConsultaStatus, set[ConsultaStatus]] = {
    ConsultaStatus.AGENDADO: {ConsultaStatus.CONFIRMADO, ConsultaStatus.CANCELADO},
    ConsultaStatus.CONFIRMADO: {
        ConsultaStatus.EM_ATENDIMENTO,
        ConsultaStatus.CANCELADO,
        ConsultaStatus.NAO_COMPARECEU,
    },
    ConsultaStatus.EM_ATENDIMENTO: {ConsultaStatus.CONCLUIDO},
    ConsultaStatus.CONCLUIDO: set(),
    ConsultaStatus.CANCELADO: set(),
    ConsultaStatus.NAO_COMPARECEU: set(),
}


class ConsultaService:
    def __init__(self, db: Session) -> None:
        self.repository = ConsultaRepository(db)
        self.animal_repository = AnimalRepository(db)
        self.tutor_repository = TutorRepository(db)
        self.veterinario_repository = VeterinarioRepository(db)
        self.prescricao_repository = PrescricaoRepository(db)
        self.history_repository = AppointmentStatusHistoryRepository(db)
        self.db = db

    def _validate_appointment_creation(
        self, data: ConsultaCreate, exclude_id: int | None = None
    ) -> None:
        animal = self.animal_repository.get_by_id(data.animal_id)
        if not animal:
            raise NotFoundException("Animal", data.animal_id)

        tutor = self.tutor_repository.get_by_id(animal.tutor_id)
        if not tutor:
            raise NotFoundException("Tutor", animal.tutor_id)

        if not tutor.ativo:
            raise OwnerInactiveException()

        if animal.obito:
            raise PetDeceasedException()

        veterinario = self.veterinario_repository.lock_by_id(data.veterinario_id)
        if not veterinario:
            raise NotFoundException("Veterinário", data.veterinario_id)

        if not veterinario.ativo:
            raise VetInactiveException()

        if data.tipo_servico == TipoServico.CIRURGIA:
            if Especialidade.CIRURGIA.value not in veterinario.especialidades:
                raise VetMissingSpecialtyException()

        overlapping = self.repository.find_overlapping_for_vet(
            veterinario_id=data.veterinario_id,
            data_hora_inicio=data.data_hora_inicio,
            data_hora_fim=data.data_hora_fim,
            exclude_id=exclude_id,
        )
        if overlapping:
            raise ScheduleConflictException(
                details={
                    "veterinario_id": data.veterinario_id,
                    "conflicting_appointments": [c.id for c in overlapping],
                }
            )

    def _validate_transition(
        self, current: ConsultaStatus, new_status: ConsultaStatus
    ) -> None:
        allowed = VALID_TRANSITIONS.get(current, set())
        if new_status not in allowed:
            raise InvalidTransitionException(current.value, new_status.value)

    def _record_status_change(
        self,
        appointment_id: int,
        old_status: ConsultaStatus | None,
        new_status: ConsultaStatus,
        changed_by: str = "system",
    ) -> None:
        self.history_repository.create(
            appointment_id=appointment_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
        )

    def _calculate_valor_total(self, consulta_id: int) -> Decimal:
        consulta = self.repository.get_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)

        prescricoes = self.prescricao_repository.get_by_consulta_id(consulta_id)
        prescricoes_total = sum(
            (p.valor_unitario * p.quantidade for p in prescricoes),
            start=Decimal("0"),
        )
        urgente_extra = (
            consulta.valor_base * Decimal("0.30") if consulta.urgente else Decimal("0")
        )
        return consulta.valor_base + prescricoes_total + urgente_extra

    def create(self, data: ConsultaCreate) -> ConsultaResponse:
        self._validate_appointment_creation(data)
        consulta = self.repository.create(data)
        self._record_status_change(
            appointment_id=consulta.id,
            old_status=None,
            new_status=ConsultaStatus.AGENDADO,
        )
        self.db.commit()
        self.db.refresh(consulta)
        return ConsultaResponse.model_validate(consulta)

    def get_by_id(self, consulta_id: int) -> ConsultaResponse:
        consulta = self.repository.get_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        return ConsultaResponse.model_validate(consulta)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: ConsultaStatus | None = None,
        animal_id: int | None = None,
        veterinario_id: int | None = None,
        tipo_servico: TipoServico | None = None,
        data_inicio: datetime | None = None,
        data_fim: datetime | None = None,
    ) -> ConsultaListResponse:
        items = self.repository.get_all(
            skip=skip,
            limit=limit,
            status=status,
            animal_id=animal_id,
            veterinario_id=veterinario_id,
            tipo_servico=tipo_servico,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
        total = self.repository.count(
            status=status,
            animal_id=animal_id,
            veterinario_id=veterinario_id,
            tipo_servico=tipo_servico,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
        return ConsultaListResponse(
            items=[ConsultaResponse.model_validate(c) for c in items],
            total=total,
            limit=limit,
            offset=skip,
        )

    def update(self, consulta_id: int, data: ConsultaUpdate) -> ConsultaResponse:
        consulta = self.repository.lock_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)

        if consulta.status in (
            ConsultaStatus.CONCLUIDO,
            ConsultaStatus.CANCELADO,
            ConsultaStatus.NAO_COMPARECEU,
        ):
            raise InvalidTransitionException(
                consulta.status.value, "UPDATE"
            )

        update_payload = data.model_dump(exclude_unset=True)
        merged = ConsultaCreate(
            animal_id=update_payload.get("animal_id", consulta.animal_id),
            veterinario_id=update_payload.get("veterinario_id", consulta.veterinario_id),
            tipo_servico=update_payload.get("tipo_servico", consulta.tipo_servico),
            data_hora_inicio=update_payload.get("data_hora_inicio", consulta.data_hora_inicio),
            data_hora_fim=update_payload.get("data_hora_fim", consulta.data_hora_fim),
            urgente=update_payload.get("urgente", consulta.urgente),
            valor_base=update_payload.get("valor_base", consulta.valor_base),
            observacoes=update_payload.get("observacoes", consulta.observacoes),
        )
        self._validate_appointment_creation(merged, exclude_id=consulta_id)

        consulta = self.repository.update(consulta, data)
        self.db.commit()
        self.db.refresh(consulta)
        return ConsultaResponse.model_validate(consulta)

    def delete(self, consulta_id: int) -> None:
        consulta = self.repository.get_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        self.repository.delete(consulta)
        self.db.commit()

    def confirm(self, consulta_id: int, changed_by: str = "system") -> ConsultaResponse:
        consulta = self.repository.lock_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        self._validate_transition(consulta.status, ConsultaStatus.CONFIRMADO)
        old_status = consulta.status
        consulta.status = ConsultaStatus.CONFIRMADO
        self._record_status_change(consulta.id, old_status, ConsultaStatus.CONFIRMADO, changed_by)
        self.db.commit()
        self.db.refresh(consulta)
        return ConsultaResponse.model_validate(consulta)

    def start(self, consulta_id: int, changed_by: str = "system") -> ConsultaResponse:
        consulta = self.repository.lock_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        self._validate_transition(consulta.status, ConsultaStatus.EM_ATENDIMENTO)
        old_status = consulta.status
        consulta.status = ConsultaStatus.EM_ATENDIMENTO
        self._record_status_change(
            consulta.id, old_status, ConsultaStatus.EM_ATENDIMENTO, changed_by
        )
        self.db.commit()
        self.db.refresh(consulta)
        return ConsultaResponse.model_validate(consulta)

    def complete(self, consulta_id: int, changed_by: str = "system") -> ConsultaResponse:
        consulta = self.repository.lock_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        self._validate_transition(consulta.status, ConsultaStatus.CONCLUIDO)
        old_status = consulta.status
        consulta.valor_total = self._calculate_valor_total(consulta_id)
        consulta.status = ConsultaStatus.CONCLUIDO
        self._record_status_change(consulta.id, old_status, ConsultaStatus.CONCLUIDO, changed_by)
        self.db.commit()
        self.db.refresh(consulta)
        return ConsultaResponse.model_validate(consulta)

    def cancel(
        self, consulta_id: int, data: ConsultaCancel, changed_by: str = "system"
    ) -> ConsultaResponse:
        if not data.motivo_cancelamento or not data.motivo_cancelamento.strip():
            raise CancellationReasonRequiredException()

        consulta = self.repository.lock_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        self._validate_transition(consulta.status, ConsultaStatus.CANCELADO)
        old_status = consulta.status
        consulta.motivo_cancelamento = data.motivo_cancelamento
        consulta.status = ConsultaStatus.CANCELADO
        self._record_status_change(consulta.id, old_status, ConsultaStatus.CANCELADO, changed_by)
        self.db.commit()
        self.db.refresh(consulta)
        return ConsultaResponse.model_validate(consulta)

    def no_show(self, consulta_id: int, changed_by: str = "system") -> ConsultaResponse:
        consulta = self.repository.lock_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        self._validate_transition(consulta.status, ConsultaStatus.NAO_COMPARECEU)
        old_status = consulta.status
        consulta.status = ConsultaStatus.NAO_COMPARECEU
        self._record_status_change(
            consulta.id, old_status, ConsultaStatus.NAO_COMPARECEU, changed_by
        )
        self.db.commit()
        self.db.refresh(consulta)
        return ConsultaResponse.model_validate(consulta)
