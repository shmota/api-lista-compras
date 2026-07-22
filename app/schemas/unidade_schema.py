from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator

from .base_schema import SchemaBase as base

class UnidadeBase(base):
    
    nome: str
    sigla: str
    
    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        return base.validar_texto(value, "O nome")
    
    @field_validator("sigla")
    @classmethod
    def validar_sigla(cls, value: str) -> str:
        return base.validar_texto(value, "A sigla", 1, 10)
    
class UnidadeResponse(base):
    id: int
    nome: str
    sigla: str
    
class UnidadeCreate(UnidadeBase):
    pass

class UnidadeUpdate(UnidadeBase):
    pass