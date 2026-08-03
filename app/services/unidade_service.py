from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.unidade_medida import UnidadeMedida
from ..repositories.unidade_repo import UnidadeRepository
from ..schemas.unidade_schema import UnidadeCreate, UnidadeUpdate
from .util import execute


class UnidadeService:
    def __init__(self, db: Session) -> None:
        self.repository = UnidadeRepository(db)

    def criar(self, unidade: UnidadeCreate) -> UnidadeMedida:

        unidade.nome = unidade.nome.lower()

        existe_sigla = self.repository.existe_sigla(unidade.sigla)
        existe_nome = self.repository.existe_nome(unidade.nome)

        if existe_sigla and existe_nome:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma unidade com esse nome e sigla.",
            )

        elif existe_nome:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma unidade com esse nome.",
            )

        elif existe_sigla:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma unidade com essa sigla.",
            )

        unidade = UnidadeMedida(nome=unidade.nome.lower(), sigla=unidade.sigla)

        unidade = execute(lambda: self.repository.criar(unidade))
        return unidade

    def listar(self, search: str | None = None) -> list[UnidadeMedida]:

        if not search:
            return self.repository.listar().all()

        elif len(search) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O campo de busca deve ter pelo menos 1 caractere.",
            )

        return self.repository.listar(
            or_(
                UnidadeMedida.nome.ilike(f"%{search}%"),
                UnidadeMedida.sigla.ilike(f"%{search}%"),
            )
        ).all()

    def listar_id(self, id: int) -> UnidadeMedida:
        return self.repository.get_by_id(id)

    def alterar(self, id: int, dados: UnidadeUpdate) -> UnidadeMedida:

        unidade = self.repository.get_by_id(id)

        if not unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A unidade informada nao existe.",
            )

        elif unidade.sigla == dados.sigla and unidade.nome == dados.nome:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Nenhuma alteração foi necessária.",
            )

        elif self.repository.existe_nome(dados.nome):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma unidade com esse nome.",
            )

        elif self.repository.existe_sigla(dados.sigla):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma unidade com essa sigla.",
            )

        unidade.sigla = dados.sigla
        unidade.nome = dados.nome.lower()

        unidade = execute(lambda: self.repository.alterar(unidade))
        return unidade

    def deletar(self, id: int) -> None:
        unidade: UnidadeMedida | None = self.repository.get_by_id(id)

        if not unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A unidade informada não existe.",
            )

        execute(lambda: self.repository.deletar(unidade))
