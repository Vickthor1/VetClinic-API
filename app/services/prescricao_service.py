from sqlalchemy.orm import Session

from app.core.exceptions import AppointmentNotInProgressException, NotFoundException
from app.models.enums import ConsultaStatus
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.prescricao_repository import PrescricaoRepository
from app.schemas.prescricao import PrescricaoCreate, PrescricaoResponse, PrescricaoUpdate


class PrescricaoService:
    def __init__(self, db: Session) -> None:
        self.repository = PrescricaoRepository(db)
        self.consulta_repository = ConsultaRepository(db)
        self.db = db

    def create(self, data: PrescricaoCreate) -> PrescricaoResponse:
        consulta = self.consulta_repository.get_by_id(data.consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", data.consulta_id)

        if consulta.status != ConsultaStatus.EM_ATENDIMENTO:
            raise AppointmentNotInProgressException()

        prescricao = self.repository.create(data)
        self.db.commit()
        return PrescricaoResponse.model_validate(prescricao)

    def get_by_id(self, prescricao_id: int) -> PrescricaoResponse:
        prescricao = self.repository.get_by_id(prescricao_id)
        if not prescricao:
            raise NotFoundException("Prescrição", prescricao_id)
        return PrescricaoResponse.model_validate(prescricao)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[PrescricaoResponse]:
        prescricoes = self.repository.get_all(skip=skip, limit=limit)
        return [PrescricaoResponse.model_validate(p) for p in prescricoes]

    def list_by_consulta(self, consulta_id: int) -> list[PrescricaoResponse]:
        consulta = self.consulta_repository.get_by_id(consulta_id)
        if not consulta:
            raise NotFoundException("Consulta", consulta_id)
        prescricoes = self.repository.get_by_consulta_id(consulta_id)
        return [PrescricaoResponse.model_validate(p) for p in prescricoes]

    def update(self, prescricao_id: int, data: PrescricaoUpdate) -> PrescricaoResponse:
        prescricao = self.repository.get_by_id(prescricao_id)
        if not prescricao:
            raise NotFoundException("Prescrição", prescricao_id)
        prescricao = self.repository.update(prescricao, data)
        self.db.commit()
        return PrescricaoResponse.model_validate(prescricao)

    def delete(self, prescricao_id: int) -> None:
        prescricao = self.repository.get_by_id(prescricao_id)
        if not prescricao:
            raise NotFoundException("Prescrição", prescricao_id)
        self.repository.delete(prescricao)
        self.db.commit()
