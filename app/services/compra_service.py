from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.compra import Compra
from ..models.item_compra import ItemCompra
from ..repositories.compra_repo import CompraRepository
from ..repositories.item_compra_repo import ItemCompraRepository
from ..repositories.produto_repo import ProdutoRepository
from ..schemas.compra_schema import CompraCreate, CompraFiltros, CompraUpdate
from .util import execute


class CompraService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = CompraRepository(db)
        self.item_repo = ItemCompraRepository(db)
        self.produto_repo = ProdutoRepository(db)

    def criar(self, dados: CompraCreate) -> Compra:
        if not dados.itens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A compra deve possuir pelo menos 1 item.",
            )

        # Validate that all referenced products exist
        for item_in in dados.itens:
            produto = self.produto_repo.get_by_id(item_in.produto_id)
            if not produto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Produto com id {item_in.produto_id} não encontrado.",
                )

        data_compra = dados.data if dados.data else datetime.now()

        compra = Compra(
            data=data_compra,
            valor_total=0.0,
        )
        compra = execute(lambda: self.repository.criar(compra))

        valor_total_compra = 0.0
        for item_in in dados.itens:
            valor_total_item = round(float(item_in.quantidade) * float(item_in.valor_unitario), 2)
            valor_total_compra += valor_total_item

            item = ItemCompra(
                compra_id=compra.id,
                produto_id=item_in.produto_id,
                quantidade=item_in.quantidade,
                valor_unitario=item_in.valor_unitario,
                valor_total=valor_total_item,
            )
            self.item_repo.criar(item)

        compra.valor_total = round(valor_total_compra, 2)
        execute(lambda: self.repository.alterar(compra))

        return self.repository.get_by_id(compra.id)

    def listar(self, filtros: CompraFiltros = None) -> list[Compra]:
        query_filters = []

        if filtros:
            if filtros.data:
                query_filters.append(func.date(Compra.data) == filtros.data)
            if filtros.data_inicio:
                query_filters.append(func.date(Compra.data) >= filtros.data_inicio)
            if filtros.data_fim:
                query_filters.append(func.date(Compra.data) <= filtros.data_fim)

        return self.repository.listar(*query_filters).all()

    def listar_id(self, id: int) -> Compra:
        compra = self.repository.get_by_id(id)
        if not compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra não encontrada.",
            )
        return compra

    def alterar(self, id: int, dados: CompraUpdate) -> Compra:
        compra = self.repository.get_by_id(id)
        if not compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra não encontrada.",
            )

        if dados.data:
            compra.data = dados.data

        execute(lambda: self.repository.alterar(compra))
        return self.repository.get_by_id(id)

    def deletar(self, id: int) -> None:
        compra = self.repository.get_by_id(id)
        if not compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra não encontrada.",
            )

        execute(lambda: self.repository.deletar(compra))

