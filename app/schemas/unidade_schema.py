from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator

from .validators import validar_texto

class SchemaBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

class UnidadeBase(SchemaBase):
    
    nome: str
    sigla: str
    
    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        return validar_texto(value, "O nome")
    
    @field_validator("sigla")
    @classmethod
    def validar_sigla(cls, value: str) -> str:
        return validar_texto(value, "A sigla", 1, 10)
    
class UnidadeResponse(SchemaBase):
    id: int
    nome: str
    sigla: str
    
class UnidadeCreate(UnidadeBase):
    pass

class UnidadeUpdate(UnidadeBase):
    pass