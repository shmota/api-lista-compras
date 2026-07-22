from pydantic import field_validator, Field, BaseModel
from fastapi import Query
from typing import Optional
from datetime import datetime

from .base_schema import SchemaBase as base
from .unidade_schema import UnidadeResponse
from .categoria_schema import CategoriaResponse

class ProdutoBase(base):
    
    nome: str
    
    @field_validator("nome")
    def validar_nome(cls, value: str) -> str:
        return base.validar_texto(value, "O nome")
        
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
    
class ProdutoFiltros(BaseModel):
    nome: Optional[str] = Field(default=None, description="Filtro por nome")
    categoria: Optional[int] = Field(default=None, description="Filtro por categoria")
    unidade: Optional[int] = Field(default=None, description="Filtro por unidade")
    em_falta: Optional[bool] = Field(default=False, description="Filtro por em falta")