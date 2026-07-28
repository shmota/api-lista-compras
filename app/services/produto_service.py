from fastapi import HTTPException, status
from sqlalchemy.orm import Session, Query
from sqlalchemy import or_

from ..models.produto import Produto
from ..repositories.produto_repo import ProdutoRepository
from ..repositories.unidade_repo import UnidadeRepository
from ..repositories.categoria_repo import CategoriaRepository
from ..schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoFiltros

from .util import execute


class ProdutoService:
    def __init__(self, db: Session) -> None:
        self.repository = ProdutoRepository(db)
        self.um = UnidadeRepository(db)
        self.ct = CategoriaRepository(db)

    def criar(self, dados: ProdutoCreate) -> ProdutoResponse:

        categoria = self.ct.get_by_id(dados.categoria_id)
        unidade = self.um.get_by_id(dados.unidade_medida_id)

        if categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoria nao encontrada"
            )

        if unidade is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Unidade nao encontrada"
            )

        produto = Produto(
            nome=dados.nome,
            categoria_id=categoria.id,
            unidade_medida_id=unidade.id,
        )

        produto = self.repository.criar(produto)

        produto = ProdutoResponse.model_validate(produto)

        return produto

    def listar(self, filtros: ProdutoFiltros = None, id: int = None) -> list[Produto] or Produto:

        if id:

            return self.repository.get_by_id(id)

        else:
            
            query = []
            
            if filtros.em_falta:
                query.append(Produto.quantidade_atual < Produto.quantidade_ideal)
                
            if filtros.categoria:
                query.append(Produto.categoria_id == filtros.categoria)
                
            if filtros.unidade:
                query.append(Produto.unidade_medida_id == filtros.unidade)
                
            if filtros.nome:
                query.append(Produto.nome.ilike(f"%{filtros.nome.lower()}%"))
                
            return self.repository.listar(*query).all()
