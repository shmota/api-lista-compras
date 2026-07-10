from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator


class CategoriaBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid",
    )
    
    @classmethod
    @field_validator("nome")
    def validar_nome(cls, value: str) -> str:
        
        min_length = 3
        max_length = 100
        
        if not value:
            raise ValueError("O nome da categoria é obrigatório.")
        elif len(value) < min_length or len(value) > max_length:
            raise ValueError(f"O nome da categoria deve ter entre {min_length} e {max_length} caracteres.")
        
        return value

class CategoriaCreate(CategoriaBase):
    nome: str
    
class CategoriaResponse(CategoriaBase):
    id: int
    nome: str
    
class CategoriaUpdate(CategoriaBase):
    id: int
    nome: str
    
class CategoriaDelete(CategoriaBase):
    id: int