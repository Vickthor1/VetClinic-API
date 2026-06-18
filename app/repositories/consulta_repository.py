from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.consulta import Consulta
from app.models.enums import ConsultaStatus, TipoServico
from app.schemas.consulta import ConsultaCreate, ConsultaUpdate


class ConsultaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: ConsultaCreate, status: ConsultaStatus = ConsultaStatus.AGENDADO) -> Consulta:
        consulta = Consulta(**data.model_dump(), status=status)
        self.db.add(consulta)
        self.db.flush()
        self.db.refresh(consulta)
        return consulta

    def get_by_id(self, consulta_id: int) -> Consulta | None:
        return self.db.get(Consulta, consulta_id)

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: ConsultaStatus | None = None,
        animal_id: int | None = None,
        veterinario_id: int | None = None,
        tipo_servico: TipoServico | None = None,
        data_inicio: datetime | None = None,
        data_fim: datetime | None = None,
    ) -> list[Consulta]:
        query = self.db.query(Consulta)

        if status is not None:
            query = query.filter(Consulta.status == status)
        if animal_id is not None:
            query = query.filter(Consulta.animal_id == animal_id)
        if veterinario_id is not None:
            query = query.filter(Consulta.veterinario_id == veterinario_id)
        if tipo_servico is not None:
            query = query.filter(Consulta.tipo_servico == tipo_servico)
        if data_inicio is not None:
            query = query.filter(Consulta.data_hora_inicio >= data_inicio)
        if data_fim is not None:
            query = query.filter(Consulta.data_hora_fim <= data_fim)

        return query.order_by(Consulta.data_hora_inicio.desc()).offset(skip).limit(limit).all()

    def count(
        self,
        status: ConsultaStatus | None = None,
        animal_id: int | None = None,
        veterinario_id: int | None = None,
        tipo_servico: TipoServico | None = None,
        data_inicio: datetime | None = None,
        data_fim: datetime | None = None,
    ) -> int:
        query = self.db.query(Consulta)

        if status is not None:
            query = query.filter(Consulta.status == status)
        if animal_id is not None:
            query = query.filter(Consulta.animal_id == animal_id)
        if veterinario_id is not None:
            query = query.filter(Consulta.veterinario_id == veterinario_id)
        if tipo_servico is not None:
            query = query.filter(Consulta.tipo_servico == tipo_servico)
        if data_inicio is not None:
            query = query.filter(Consulta.data_hora_inicio >= data_inicio)
        if data_fim is not None:
            query = query.filter(Consulta.data_hora_fim <= data_fim)

        return query.count()

    def update(self, consulta: Consulta, data: ConsultaUpdate) -> Consulta:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(consulta, field, value)
        self.db.flush()
        self.db.refresh(consulta)
        return consulta

    def delete(self, consulta: Consulta) -> None:
        self.db.delete(consulta)
        self.db.flush()

    def find_overlapping_for_vet(
        self,
        veterinario_id: int,
        data_hora_inicio: datetime,
        data_hora_fim: datetime,
        exclude_id: int | None = None,
    ) -> list[Consulta]:
        query = (
            self.db.query(Consulta)
            .filter(
                Consulta.veterinario_id == veterinario_id,
                Consulta.status.notin_(
                    [ConsultaStatus.CANCELADO, ConsultaStatus.NAO_COMPARECEU]
                ),
                or_(
                    and_(
                        Consulta.data_hora_inicio < data_hora_fim,
                        Consulta.data_hora_fim > data_hora_inicio,
                    )
                ),
            )
            .with_for_update()
        )
        if exclude_id is not None:
            query = query.filter(Consulta.id != exclude_id)
        return query.all()

    def lock_by_id(self, consulta_id: int) -> Consulta | None:
        return (
            self.db.query(Consulta)
            .filter(Consulta.id == consulta_id)
            .with_for_update()
            .first()
        )
