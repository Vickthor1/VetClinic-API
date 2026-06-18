from sqlalchemy.orm import Session

from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate


class TutorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: TutorCreate) -> Tutor:
        tutor = Tutor(**data.model_dump())
        self.db.add(tutor)
        self.db.flush()
        self.db.refresh(tutor)
        return tutor

    def get_by_id(self, tutor_id: int) -> Tutor | None:
        return self.db.get(Tutor, tutor_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Tutor]:
        return self.db.query(Tutor).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Tutor).count()

    def update(self, tutor: Tutor, data: TutorUpdate) -> Tutor:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(tutor, field, value)
        self.db.flush()
        self.db.refresh(tutor)
        return tutor

    def delete(self, tutor: Tutor) -> None:
        self.db.delete(tutor)
        self.db.flush()
