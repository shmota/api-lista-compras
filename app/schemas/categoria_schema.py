from .base_schema import SchemaBase
from pydantic import Field, field_validator

class CategoriaCreate(SchemaBase):
    nome: str = Field(
        min_length=3,
        max_length=100,
        description="Nome da categoria",
    )
    
    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        if not value:
            raise ValueError("O nome da categoria é obrigatório.")
        return value
    
class CategoriaResponse(SchemaBase):
    id: int
    nome: str