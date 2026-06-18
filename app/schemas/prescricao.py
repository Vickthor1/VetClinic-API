from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PrescricaoCreate(BaseModel):
    consulta_id: int
    medicamento: str = Field(..., min_length=1, max_length=255)
    dosagem: str = Field(..., min_length=1, max_length=100)
    quantidade: int = Field(..., gt=0)
    frequencia: str = Field(..., min_length=1, max_length=100)
    duracao_dias: int = Field(..., gt=0)
    valor_unitario: Decimal = Field(..., ge=0)
    observacoes: str | None = None


class PrescricaoUpdate(BaseModel):
    medicamento: str | None = Field(None, min_length=1, max_length=255)
    dosagem: str | None = Field(None, min_length=1, max_length=100)
    quantidade: int | None = Field(None, gt=0)
    frequencia: str | None = Field(None, min_length=1, max_length=100)
    duracao_dias: int | None = Field(None, gt=0)
    valor_unitario: Decimal | None = Field(None, ge=0)
    observacoes: str | None = None


class PrescricaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    consulta_id: int
    medicamento: str
    dosagem: str
    quantidade: int
    frequencia: str
    duracao_dias: int
    valor_unitario: Decimal
    observacoes: str | None
    created_at: datetime
