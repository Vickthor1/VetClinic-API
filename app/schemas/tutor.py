import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class TutorCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    cpf: str = Field(..., min_length=11, max_length=11)
    email: EmailStr
    telefone: str = Field(..., min_length=8, max_length=20)
    ativo: bool = True

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        if not re.fullmatch(r"\d{11}", value):
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        return value


class TutorUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=255)
    cpf: str | None = Field(None, min_length=11, max_length=11)
    email: EmailStr | None = None
    telefone: str | None = Field(None, min_length=8, max_length=20)
    ativo: bool | None = None

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str | None) -> str | None:
        if value is not None and not re.fullmatch(r"\d{11}", value):
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        return value


class TutorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cpf: str
    email: str
    telefone: str
    ativo: bool
    created_at: datetime
    updated_at: datetime
