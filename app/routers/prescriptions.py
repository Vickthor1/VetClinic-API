from fastapi import APIRouter, Query, status

from app.core.dependencies import DbSession
from app.schemas.prescricao import PrescricaoCreate, PrescricaoResponse, PrescricaoUpdate
from app.services.prescricao_service import PrescricaoService

router = APIRouter(prefix="/prescriptions", tags=["Prescrições"])


@router.post("", response_model=PrescricaoResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(data: PrescricaoCreate, db: DbSession) -> PrescricaoResponse:
    return PrescricaoService(db).create(data)


@router.get("", response_model=list[PrescricaoResponse])
def list_prescriptions(
    db: DbSession,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[PrescricaoResponse]:
    return PrescricaoService(db).list_all(skip=offset, limit=limit)


@router.get("/by-appointment/{consulta_id}", response_model=list[PrescricaoResponse])
def list_prescriptions_by_appointment(
    consulta_id: int, db: DbSession
) -> list[PrescricaoResponse]:
    return PrescricaoService(db).list_by_consulta(consulta_id)


@router.get("/{prescription_id}", response_model=PrescricaoResponse)
def get_prescription(prescription_id: int, db: DbSession) -> PrescricaoResponse:
    return PrescricaoService(db).get_by_id(prescription_id)


@router.put("/{prescription_id}", response_model=PrescricaoResponse)
def update_prescription(
    prescription_id: int, data: PrescricaoUpdate, db: DbSession
) -> PrescricaoResponse:
    return PrescricaoService(db).update(prescription_id, data)


@router.delete("/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prescription(prescription_id: int, db: DbSession) -> None:
    PrescricaoService(db).delete(prescription_id)
