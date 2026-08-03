from pydantic import field_validator, Field, BaseModel
from fastapi import Query
from datetime import datetime

from .base_schema import SchemaBase as base
from .unidade_schema import UnidadeResponse
from .categoria_schema import CategoriaResponse

class ProdutoBase(base):
    
    nome: str
    quantidade_atual: float = 0
    quantidade_ideal: float = 0
    
    @field_validator("nome")
    def validar_nome(cls, value: str) -> str:
        return base.validar_texto(value, "O nome")
    
    @field_validator("quantidade_atual")
    def validar_quantidade_atual(cls, value: float) -> float:
        if value < 0:
            raise ValueError("A quantidade atual deve ser maior ou igual a zero.")
        return value
    
    @field_validator("quantidade_ideal")
    def validar_quantidade_ideal(cls, value: float) -> float:
        if value < 0:
            raise ValueError("A quantidade ideal deve ser maior ou igual a zero.")
        return value
        
class ProdutoResponse(base):
    id: int
    nome: str
    categoria: CategoriaResponse
    unidade_medida: UnidadeResponse
    quantidade_atual: float
    quantidade_ideal: float
    observacao: str
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
    
class ProdutoCreate(ProdutoBase):
    categoria_id: int
    unidade_medida_id: int
    
class ProdutoUpdate(ProdutoBase):
    categoria_id: int
    unidade_medida_id: int
    observacao: str | None = Field(default=None)
    ativo: bool | None = Field(default=None)
    
class ProdutoFiltros(BaseModel):
    nome: str = Field(default=None, description="Filtro por nome")
    categoria: int = Field(default=None, description="Filtro por categoria")
    unidade: int = Field(default=None, description="Filtro por unidade")
    em_falta: bool = Field(default=False, description="Filtro por em falta")