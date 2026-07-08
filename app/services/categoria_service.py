from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.repositories.categoria_repo import CategoriaRepository
from app.schemas.categoria_schema import CategoriaCreate


class CategoriaService:

    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def criar(self, dados: CategoriaCreate) -> Categoria:

        categoria_existente = self.repository.buscar_por_nome(
            dados.nome
        )

        if categoria_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma categoria com esse nome."
            )

        categoria = Categoria(
            nome=dados.nome
        )
        
        try:
            categoria = self.repository.criar(categoria)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        return categoria
    
    def listar(self) -> list[Categoria]:
        return self.repository.listar()
    
    def buscar_por_nome(self, nome: str) -> Categoria | None:
        return self.repository.listar(Categoria.nome == Categoria.nome.like(f"%{nome}%"))