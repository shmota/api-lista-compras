from pydantic import Field, field_validator

from .base_schema import SchemaBase as base

class CategoriaBase(base):
    nome: str
    
    @classmethod
    @field_validator("nome")
    def validar_nome(cls, value: str) -> str:
        
        return base.validar_texto(value, "O nome")

class CategoriaCreate(CategoriaBase):
    pass
    
class CategoriaResponse(base):
    id: int
    nome: str
    
class CategoriaUpdate(CategoriaBase):
    pass