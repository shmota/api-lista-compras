from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator


class ProdutoBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    @field_validator("nome")
    def validar_nome(cls, value: str) -> str:
        min_length = 3
        max_length = 100
        
        value = value.strip()

        if not value:
            raise ValueError("O nome do produto é obrigatório.")
        elif len(value) < min_length or len(value) > max_length:
            raise ValueError(
                f"O nome do produto deve ter entre {min_length} e {max_length} caracteres."
            )

        return value
    
class ProdutoCreate(ProdutoBase):
    unidade_medida_id: int