from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.repositories.animal_repository import AnimalRepository
from app.repositories.tutor_repository import TutorRepository
from app.schemas.animal import AnimalCreate, AnimalResponse, AnimalUpdate


class AnimalService:
    def __init__(self, db: Session) -> None:
        self.repository = AnimalRepository(db)
        self.tutor_repository = TutorRepository(db)
        self.db = db

    def create(self, data: AnimalCreate) -> AnimalResponse:
        tutor = self.tutor_repository.get_by_id(data.tutor_id)
        if not tutor:
            raise NotFoundException("Tutor", data.tutor_id)
        animal = self.repository.create(data)
        self.db.commit()
        return AnimalResponse.model_validate(animal)

    def get_by_id(self, animal_id: int) -> AnimalResponse:
        animal = self.repository.get_by_id(animal_id)
        if not animal:
            raise NotFoundException("Animal", animal_id)
        return AnimalResponse.model_validate(animal)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[AnimalResponse]:
        animals = self.repository.get_all(skip=skip, limit=limit)
        return [AnimalResponse.model_validate(a) for a in animals]

    def update(self, animal_id: int, data: AnimalUpdate) -> AnimalResponse:
        animal = self.repository.get_by_id(animal_id)
        if not animal:
            raise NotFoundException("Animal", animal_id)
        if data.tutor_id is not None:
            tutor = self.tutor_repository.get_by_id(data.tutor_id)
            if not tutor:
                raise NotFoundException("Tutor", data.tutor_id)
        animal = self.repository.update(animal, data)
        self.db.commit()
        return AnimalResponse.model_validate(animal)

    def delete(self, animal_id: int) -> None:
        animal = self.repository.get_by_id(animal_id)
        if not animal:
            raise NotFoundException("Animal", animal_id)
        self.repository.delete(animal)
        self.db.commit()
