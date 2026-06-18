from datetime import datetime

from fastapi import APIRouter, Query, status

from app.core.dependencies import DbSession
from app.models.enums import ConsultaStatus, TipoServico
from app.schemas.consulta import (
    ConsultaCancel,
    ConsultaCreate,
    ConsultaListResponse,
    ConsultaResponse,
    ConsultaUpdate,
)
from app.services.consulta_service import ConsultaService

router = APIRouter(prefix="/appointments", tags=["Consultas"])


@router.post("", response_model=ConsultaResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(data: ConsultaCreate, db: DbSession) -> ConsultaResponse:
    return ConsultaService(db).create(data)


@router.get("", response_model=ConsultaListResponse)
def list_appointments(
    db: DbSession,
    status_filter: ConsultaStatus | None = Query(None, alias="status"),
    animal_id: int | None = None,
    veterinario_id: int | None = None,
    tipo_servico: TipoServico | None = None,
    data_inicio: datetime | None = None,
    data_fim: datetime | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> ConsultaListResponse:
    return ConsultaService(db).list_all(
        skip=offset,
        limit=limit,
        status=status_filter,
        animal_id=animal_id,
        veterinario_id=veterinario_id,
        tipo_servico=tipo_servico,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


@router.get("/{appointment_id}", response_model=ConsultaResponse)
def get_appointment(appointment_id: int, db: DbSession) -> ConsultaResponse:
    return ConsultaService(db).get_by_id(appointment_id)


@router.put("/{appointment_id}", response_model=ConsultaResponse)
def update_appointment(
    appointment_id: int, data: ConsultaUpdate, db: DbSession
) -> ConsultaResponse:
    return ConsultaService(db).update(appointment_id, data)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: DbSession) -> None:
    ConsultaService(db).delete(appointment_id)


@router.post("/{appointment_id}/confirm", response_model=ConsultaResponse)
def confirm_appointment(appointment_id: int, db: DbSession) -> ConsultaResponse:
    return ConsultaService(db).confirm(appointment_id)


@router.post("/{appointment_id}/start", response_model=ConsultaResponse)
def start_appointment(appointment_id: int, db: DbSession) -> ConsultaResponse:
    return ConsultaService(db).start(appointment_id)


@router.post("/{appointment_id}/complete", response_model=ConsultaResponse)
def complete_appointment(appointment_id: int, db: DbSession) -> ConsultaResponse:
    return ConsultaService(db).complete(appointment_id)


@router.post("/{appointment_id}/cancel", response_model=ConsultaResponse)
def cancel_appointment(
    appointment_id: int, data: ConsultaCancel, db: DbSession
) -> ConsultaResponse:
    return ConsultaService(db).cancel(appointment_id, data)


@router.post("/{appointment_id}/no-show", response_model=ConsultaResponse)
def no_show_appointment(appointment_id: int, db: DbSession) -> ConsultaResponse:
    return ConsultaService(db).no_show(appointment_id)
