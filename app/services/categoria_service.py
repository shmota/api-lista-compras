from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.categoria import Categoria
from ..repositories.categoria_repo import CategoriaRepository
from ..schemas.categoria_schema import CategoriaCreate, CategoriaUpdate
from .util import execute


class CategoriaService:
    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def criar(self, dados: CategoriaCreate) -> Categoria:

        if self.repository.existe_nome(dados.nome):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma categoria com esse nome.",
            )

        categoria = Categoria(nome=dados.nome)

        categoria = execute(lambda: self.repository.criar(categoria))

        return categoria

    def listar(self, dado: str | None = None) -> list[Categoria]:

        if dado:
            try:
                dado = int(dado)
                return self.repository.listar(Categoria.id == dado).all()
            except ValueError:
                return self.repository.listar(Categoria.nome.ilike(f"%{dado.lower()}%")).all()
        else:
            return self.repository.listar().all()

    def listar_id(self, id: int) -> Categoria:
        categoria: Categoria | None = self.repository.get_by_id(id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A categoria informada não existe.",
            )
        return categoria


    def alterar(self, id: int, dados: CategoriaUpdate) -> Categoria:

        categoria: Categoria | None = self.repository.listar(Categoria.id == id).first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A categoria informada não existe.",
            )

        elif categoria.nome == dados.nome:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O novo nome não pode ser igual ao atual.",
            )

        elif self.repository.existe_nome(dados.nome):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma categoria com esse nome.",
            )

        categoria.nome = dados.nome.lower()

        categoria = execute(lambda: self.repository.alterar(categoria))

        return categoria

    def deletar(self, id: int) -> None:
        categoria: Categoria | None = self.repository.get_by_id(id)

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A categoria informada não existe.",
            )

        execute(lambda: self.repository.deletar(categoria))
