from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import Especialidade


class VeterinarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    crmv: str = Field(..., min_length=4, max_length=20)
    especialidades: list[Especialidade] = Field(..., min_length=1)
    ativo: bool = True

    @field_validator("especialidades")
    @classmethod
    def validate_unique_specialties(
        cls, value: list[Especialidade]
    ) -> list[Especialidade]:
        if len(value) != len(set(value)):
            raise ValueError("Especialidades duplicadas não são permitidas.")
        return value


class VeterinarioUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=255)
    crmv: str | None = Field(None, min_length=4, max_length=20)
    especialidades: list[Especialidade] | None = Field(None, min_length=1)
    ativo: bool | None = None

    @field_validator("especialidades")
    @classmethod
    def validate_unique_specialties(
        cls, value: list[Especialidade] | None
    ) -> list[Especialidade] | None:
        if value is not None and len(value) != len(set(value)):
            raise ValueError("Especialidades duplicadas não são permitidas.")
        return value


class VeterinarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    crmv: str
    especialidades: list[str]
    ativo: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("especialidades", mode="before")
    @classmethod
    def normalize_specialties(cls, value: list) -> list[str]:
        return [item.value if hasattr(item, "value") else str(item) for item in value]
