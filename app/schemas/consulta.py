from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import ConsultaStatus, TipoServico


class ConsultaCreate(BaseModel):
    animal_id: int
    veterinario_id: int
    tipo_servico: TipoServico
    data_hora_inicio: datetime
    data_hora_fim: datetime
    urgente: bool = False
    valor_base: Decimal = Field(..., ge=0)
    observacoes: str | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> "ConsultaCreate":
        if self.data_hora_fim <= self.data_hora_inicio:
            raise ValueError("data_hora_fim deve ser posterior a data_hora_inicio.")
        return self


class ConsultaUpdate(BaseModel):
    animal_id: int | None = None
    veterinario_id: int | None = None
    tipo_servico: TipoServico | None = None
    data_hora_inicio: datetime | None = None
    data_hora_fim: datetime | None = None
    urgente: bool | None = None
    valor_base: Decimal | None = Field(None, ge=0)
    observacoes: str | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> "ConsultaUpdate":
        if (
            self.data_hora_inicio is not None
            and self.data_hora_fim is not None
            and self.data_hora_fim <= self.data_hora_inicio
        ):
            raise ValueError("data_hora_fim deve ser posterior a data_hora_inicio.")
        return self


class ConsultaCancel(BaseModel):
    motivo_cancelamento: str = Field(..., min_length=3)


class ConsultaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_id: int
    veterinario_id: int
    tipo_servico: TipoServico
    status: ConsultaStatus
    data_hora_inicio: datetime
    data_hora_fim: datetime
    urgente: bool
    valor_base: Decimal
    valor_total: Decimal | None
    motivo_cancelamento: str | None
    observacoes: str | None
    created_at: datetime
    updated_at: datetime


class ConsultaListResponse(BaseModel):
    items: list[ConsultaResponse]
    total: int
    limit: int
    offset: int
