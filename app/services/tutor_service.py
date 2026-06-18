from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.repositories.tutor_repository import TutorRepository
from app.schemas.tutor import TutorCreate, TutorResponse, TutorUpdate


class TutorService:
    def __init__(self, db: Session) -> None:
        self.repository = TutorRepository(db)
        self.db = db

    def create(self, data: TutorCreate) -> TutorResponse:
        tutor = self.repository.create(data)
        self.db.commit()
        return TutorResponse.model_validate(tutor)

    def get_by_id(self, tutor_id: int) -> TutorResponse:
        tutor = self.repository.get_by_id(tutor_id)
        if not tutor:
            raise NotFoundException("Tutor", tutor_id)
        return TutorResponse.model_validate(tutor)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[TutorResponse]:
        tutors = self.repository.get_all(skip=skip, limit=limit)
        return [TutorResponse.model_validate(t) for t in tutors]

    def update(self, tutor_id: int, data: TutorUpdate) -> TutorResponse:
        tutor = self.repository.get_by_id(tutor_id)
        if not tutor:
            raise NotFoundException("Tutor", tutor_id)
        tutor = self.repository.update(tutor, data)
        self.db.commit()
        return TutorResponse.model_validate(tutor)

    def delete(self, tutor_id: int) -> None:
        tutor = self.repository.get_by_id(tutor_id)
        if not tutor:
            raise NotFoundException("Tutor", tutor_id)
        self.repository.delete(tutor)
        self.db.commit()
