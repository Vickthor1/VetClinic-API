from fastapi import APIRouter, Query, status

from app.core.dependencies import DbSession
from app.schemas.animal import AnimalCreate, AnimalResponse, AnimalUpdate
from app.services.animal_service import AnimalService

router = APIRouter(prefix="/animals", tags=["Animais"])


@router.post("", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(data: AnimalCreate, db: DbSession) -> AnimalResponse:
    return AnimalService(db).create(data)


@router.get("", response_model=list[AnimalResponse])
def list_animals(
    db: DbSession,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[AnimalResponse]:
    return AnimalService(db).list_all(skip=offset, limit=limit)


@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(animal_id: int, db: DbSession) -> AnimalResponse:
    return AnimalService(db).get_by_id(animal_id)


@router.put("/{animal_id}", response_model=AnimalResponse)
def update_animal(animal_id: int, data: AnimalUpdate, db: DbSession) -> AnimalResponse:
    return AnimalService(db).update(animal_id, data)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(animal_id: int, db: DbSession) -> None:
    AnimalService(db).delete(animal_id)
