from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import Especie


class AnimalCreate(BaseModel):
    tutor_id: int
    nome: str = Field(..., min_length=1, max_length=255)
    especie: Especie
    raca: str = Field(..., min_length=1, max_length=100)
    peso_kg: Decimal = Field(..., gt=0)
    data_nascimento: date
    ativo: bool = True
    obito: bool = False
    data_obito: date | None = None

    @model_validator(mode="after")
    def validate_obito(self) -> "AnimalCreate":
        if self.obito and self.data_obito is None:
            raise ValueError("data_obito é obrigatória quando obito=True.")
        if not self.obito and self.data_obito is not None:
            raise ValueError("data_obito só pode ser informada quando obito=True.")
        if self.data_obito and self.data_obito > date.today():
            raise ValueError("data_obito não pode ser futura.")
        return self


class AnimalUpdate(BaseModel):
    tutor_id: int | None = None
    nome: str | None = Field(None, min_length=1, max_length=255)
    especie: Especie | None = None
    raca: str | None = Field(None, min_length=1, max_length=100)
    peso_kg: Decimal | None = Field(None, gt=0)
    data_nascimento: date | None = None
    ativo: bool | None = None
    obito: bool | None = None
    data_obito: date | None = None

    @model_validator(mode="after")
    def validate_obito(self) -> "AnimalUpdate":
        if self.obito is True and self.data_obito is None:
            raise ValueError("data_obito é obrigatória quando obito=True.")
        return self


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tutor_id: int
    nome: str
    especie: Especie
    raca: str
    peso_kg: Decimal
    data_nascimento: date
    ativo: bool
    obito: bool
    data_obito: date | None
    created_at: datetime
    updated_at: datetime
