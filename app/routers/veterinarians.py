from fastapi import APIRouter, Query, status

from app.core.dependencies import DbSession
from app.schemas.veterinario import VeterinarioCreate, VeterinarioResponse, VeterinarioUpdate
from app.services.veterinario_service import VeterinarioService

router = APIRouter(prefix="/veterinarians", tags=["Veterinários"])


@router.post("", response_model=VeterinarioResponse, status_code=status.HTTP_201_CREATED)
def create_veterinarian(data: VeterinarioCreate, db: DbSession) -> VeterinarioResponse:
    return VeterinarioService(db).create(data)


@router.get("", response_model=list[VeterinarioResponse])
def list_veterinarians(
    db: DbSession,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[VeterinarioResponse]:
    return VeterinarioService(db).list_all(skip=offset, limit=limit)


@router.get("/{veterinario_id}", response_model=VeterinarioResponse)
def get_veterinarian(veterinario_id: int, db: DbSession) -> VeterinarioResponse:
    return VeterinarioService(db).get_by_id(veterinario_id)


@router.put("/{veterinario_id}", response_model=VeterinarioResponse)
def update_veterinarian(
    veterinario_id: int, data: VeterinarioUpdate, db: DbSession
) -> VeterinarioResponse:
    return VeterinarioService(db).update(veterinario_id, data)


@router.delete("/{veterinario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_veterinarian(veterinario_id: int, db: DbSession) -> None:
    VeterinarioService(db).delete(veterinario_id)
