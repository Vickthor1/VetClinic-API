from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate


class AnimalRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: AnimalCreate) -> Animal:
        animal = Animal(**data.model_dump())
        self.db.add(animal)
        self.db.flush()
        self.db.refresh(animal)
        return animal

    def get_by_id(self, animal_id: int) -> Animal | None:
        return self.db.get(Animal, animal_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Animal]:
        return self.db.query(Animal).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Animal).count()

    def update(self, animal: Animal, data: AnimalUpdate) -> Animal:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(animal, field, value)
        self.db.flush()
        self.db.refresh(animal)
        return animal

    def delete(self, animal: Animal) -> None:
        self.db.delete(animal)
        self.db.flush()
