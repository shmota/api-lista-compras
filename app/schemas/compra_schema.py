from datetime import date, datetime

from pydantic import BaseModel, Field

from .base_schema import SchemaBase as base
from .item_compra_schema import ItemCompraCreateInput, ItemCompraResponse


class CompraCreate(base):
    data: datetime | None = Field(default=None, description="Data da compra. Se omitida, usará a data/hora atual.")
    itens: list[ItemCompraCreateInput] = Field(..., min_length=1, description="Lista de itens pertencentes a esta compra.")


class CompraUpdate(base):
    data: datetime | None = Field(default=None, description="Nova data da compra.")


class CompraResponse(base):
    id: int
    data: datetime
    valor_total: float
    creado_em: datetime
    itens: list[ItemCompraResponse] = Field(default_factory=list, description="Lista de itens pertencentes a esta compra.")


class CompraFiltros(BaseModel):
    data: date | None = Field(default=None, description="Filtro por data exata (YYYY-MM-DD)")
    data_inicio: date | None = Field(default=None, description="Filtro por data inicial (YYYY-MM-DD)")
    data_fim: date | None = Field(default=None, description="Filtro por data final (YYYY-MM-DD)")
