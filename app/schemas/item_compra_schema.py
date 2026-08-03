from pydantic import Field, field_validator

from .base_schema import SchemaBase as base
from .produto_schema import ProdutoResponse


class ItemCompraBase(base):
    produto_id: int
    quantidade: float
    valor_unitario: float

    @field_validator("quantidade")
    def validar_quantidade(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return value

    @field_validator("valor_unitario")
    def validar_valor_unitario(cls, value: float) -> float:
        if value < 0:
            raise ValueError("O valor unitário deve ser maior ou igual a zero.")
        return value


class ItemCompraCreateInput(ItemCompraBase):
    pass


class ItemCompraCreate(ItemCompraBase):
    compra_id: int


class ItemCompraUpdate(base):
    produto_id: int | None = Field(default=None)
    quantidade: float | None = Field(default=None)
    valor_unitario: float | None = Field(default=None)

    @field_validator("quantidade")
    def validar_quantidade(cls, value: float | None) -> float | None:
        if value is not None and value <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return value

    @field_validator("valor_unitario")
    def validar_valor_unitario(cls, value: float | None) -> float | None:
        if value is not None and value < 0:
            raise ValueError("O valor unitário deve ser maior ou igual a zero.")
        return value


class ItemCompraResponse(base):
    id: int
    compra_id: int
    produto_id: int
    produto: ProdutoResponse | None = None
    quantidade: float
    valor_unitario: float
    valor_total: float

