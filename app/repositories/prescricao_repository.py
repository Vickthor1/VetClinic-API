from sqlalchemy.orm import Session

from app.models.prescricao import Prescricao
from app.schemas.prescricao import PrescricaoCreate, PrescricaoUpdate


class PrescricaoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: PrescricaoCreate) -> Prescricao:
        prescricao = Prescricao(**data.model_dump())
        self.db.add(prescricao)
        self.db.flush()
        self.db.refresh(prescricao)
        return prescricao

    def get_by_id(self, prescricao_id: int) -> Prescricao | None:
        return self.db.get(Prescricao, prescricao_id)

    def get_by_consulta_id(self, consulta_id: int) -> list[Prescricao]:
        return (
            self.db.query(Prescricao)
            .filter(Prescricao.consulta_id == consulta_id)
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prescricao]:
        return self.db.query(Prescricao).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Prescricao).count()

    def update(self, prescricao: Prescricao, data: PrescricaoUpdate) -> Prescricao:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(prescricao, field, value)
        self.db.flush()
        self.db.refresh(prescricao)
        return prescricao

    def delete(self, prescricao: Prescricao) -> None:
        self.db.delete(prescricao)
        self.db.flush()
