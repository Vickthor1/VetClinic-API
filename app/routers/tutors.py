from fastapi import APIRouter, Query, status

from app.core.dependencies import DbSession
from app.schemas.tutor import TutorCreate, TutorResponse, TutorUpdate
from app.services.tutor_service import TutorService

router = APIRouter(prefix="/tutors", tags=["Tutores"])


@router.post("", response_model=TutorResponse, status_code=status.HTTP_201_CREATED)
def create_tutor(data: TutorCreate, db: DbSession) -> TutorResponse:
    return TutorService(db).create(data)


@router.get("", response_model=list[TutorResponse])
def list_tutors(
    db: DbSession,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[TutorResponse]:
    return TutorService(db).list_all(skip=offset, limit=limit)


@router.get("/{tutor_id}", response_model=TutorResponse)
def get_tutor(tutor_id: int, db: DbSession) -> TutorResponse:
    return TutorService(db).get_by_id(tutor_id)


@router.put("/{tutor_id}", response_model=TutorResponse)
def update_tutor(tutor_id: int, data: TutorUpdate, db: DbSession) -> TutorResponse:
    return TutorService(db).update(tutor_id, data)


@router.delete("/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tutor(tutor_id: int, db: DbSession) -> None:
    TutorService(db).delete(tutor_id)
