from fastapi import HTTPException, status
from sqlalchemy.orm import Session, Query

from app.models.categoria import Categoria
from app.repositories.categoria_repo import CategoriaRepository
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate


class CategoriaService:

    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def criar(self, dados: CategoriaCreate) -> Categoria:

        categoria_existente = self.repository.listar(
            Categoria.nome == dados.nome.upper()
        ).first()

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
    
    def listar(self, nome: str = None) -> list[Categoria]:
        
        if nome:
            return self.repository.listar(Categoria.nome.ilike(f"%{nome.lower()}%"))
        else:
            return self.repository.listar()
    
    def alterar(self, dados: CategoriaUpdate) -> Categoria:
        
        categoria: Categoria | None = self.repository.listar(
            Categoria.id == dados.id
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A categoria informada não existe."
            )
            
        elif categoria.nome == dados.nome:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O novo nome não pode ser igual ao atual."
            )
            
        elif self.repository.listar(Categoria.nome == dados.nome).all():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma categoria com esse nome."
            )
            
        categoria.nome = dados.nome
        
        try:
            categoria = self.repository.alterar(categoria)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        return categoria