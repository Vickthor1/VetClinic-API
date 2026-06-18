from sqlalchemy.orm import Session

from app.models.veterinario import Veterinario
from app.schemas.veterinario import VeterinarioCreate, VeterinarioUpdate


class VeterinarioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: VeterinarioCreate) -> Veterinario:
        payload = data.model_dump()
        payload["especialidades"] = [e.value for e in data.especialidades]
        veterinario = Veterinario(**payload)
        self.db.add(veterinario)
        self.db.flush()
        self.db.refresh(veterinario)
        return veterinario

    def get_by_id(self, veterinario_id: int) -> Veterinario | None:
        return self.db.get(Veterinario, veterinario_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Veterinario]:
        return self.db.query(Veterinario).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Veterinario).count()

    def update(self, veterinario: Veterinario, data: VeterinarioUpdate) -> Veterinario:
        update_data = data.model_dump(exclude_unset=True)
        if "especialidades" in update_data and update_data["especialidades"] is not None:
            update_data["especialidades"] = [e.value for e in data.especialidades or []]
        for field, value in update_data.items():
            setattr(veterinario, field, value)
        self.db.flush()
        self.db.refresh(veterinario)
        return veterinario

    def delete(self, veterinario: Veterinario) -> None:
        self.db.delete(veterinario)
        self.db.flush()

    def lock_by_id(self, veterinario_id: int) -> Veterinario | None:
        return (
            self.db.query(Veterinario)
            .filter(Veterinario.id == veterinario_id)
            .with_for_update()
            .first()
        )
