from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.repositories.veterinario_repository import VeterinarioRepository
from app.schemas.veterinario import VeterinarioCreate, VeterinarioResponse, VeterinarioUpdate


class VeterinarioService:
    def __init__(self, db: Session) -> None:
        self.repository = VeterinarioRepository(db)
        self.db = db

    def create(self, data: VeterinarioCreate) -> VeterinarioResponse:
        veterinario = self.repository.create(data)
        self.db.commit()
        return VeterinarioResponse.model_validate(veterinario)

    def get_by_id(self, veterinario_id: int) -> VeterinarioResponse:
        veterinario = self.repository.get_by_id(veterinario_id)
        if not veterinario:
            raise NotFoundException("Veterinário", veterinario_id)
        return VeterinarioResponse.model_validate(veterinario)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[VeterinarioResponse]:
        veterinarios = self.repository.get_all(skip=skip, limit=limit)
        return [VeterinarioResponse.model_validate(v) for v in veterinarios]

    def update(self, veterinario_id: int, data: VeterinarioUpdate) -> VeterinarioResponse:
        veterinario = self.repository.get_by_id(veterinario_id)
        if not veterinario:
            raise NotFoundException("Veterinário", veterinario_id)
        veterinario = self.repository.update(veterinario, data)
        self.db.commit()
        return VeterinarioResponse.model_validate(veterinario)

    def delete(self, veterinario_id: int) -> None:
        veterinario = self.repository.get_by_id(veterinario_id)
        if not veterinario:
            raise NotFoundException("Veterinário", veterinario_id)
        self.repository.delete(veterinario)
        self.db.commit()
