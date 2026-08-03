from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.item_compra import ItemCompra
from ..repositories.compra_repo import CompraRepository
from ..repositories.item_compra_repo import ItemCompraRepository
from ..repositories.produto_repo import ProdutoRepository
from ..schemas.item_compra_schema import ItemCompraCreate, ItemCompraUpdate
from .util import execute


class ItemCompraService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = ItemCompraRepository(db)
        self.compra_repo = CompraRepository(db)
        self.produto_repo = ProdutoRepository(db)

    def _recalcular_compra(self, compra_id: int) -> None:
        compra = self.compra_repo.get_by_id(compra_id)
        if compra:
            itens = self.repository.listar(ItemCompra.compra_id == compra_id).all()
            valor_total_calculado = sum(
                (float(item.valor_total) for item in itens),
                start=0.0
            )
            compra.valor_total = round(valor_total_calculado, 2)
            self.compra_repo.alterar(compra)

    def criar(self, dados: ItemCompraCreate) -> ItemCompra:
        compra = self.compra_repo.get_by_id(dados.compra_id)
        if not compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra não encontrada.",
            )

        produto = self.produto_repo.get_by_id(dados.produto_id)
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado.",
            )

        valor_total_item = round(float(dados.quantidade) * float(dados.valor_unitario), 2)

        item = ItemCompra(
            compra_id=dados.compra_id,
            produto_id=dados.produto_id,
            quantidade=dados.quantidade,
            valor_unitario=dados.valor_unitario,
            valor_total=valor_total_item,
        )

        item = execute(lambda: self.repository.criar(item))
        self._recalcular_compra(dados.compra_id)

        return self.repository.get_by_id(item.id)

    def listar(self, compra_id: int | None = None) -> list[ItemCompra]:
        if compra_id:
            return self.repository.listar(ItemCompra.compra_id == compra_id).all()
        return self.repository.listar().all()

    def listar_id(self, id: int) -> ItemCompra:
        item = self.repository.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de compra não encontrado.",
            )
        return item

    def alterar(self, id: int, dados: ItemCompraUpdate) -> ItemCompra:
        item = self.repository.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de compra não encontrado.",
            )

        if dados.produto_id is not None:
            produto = self.produto_repo.get_by_id(dados.produto_id)
            if not produto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Produto não encontrado.",
                )
            item.produto_id = dados.produto_id

        if dados.quantidade is not None:
            item.quantidade = dados.quantidade

        if dados.valor_unitario is not None:
            item.valor_unitario = dados.valor_unitario

        item.valor_total = round(float(item.quantidade) * float(item.valor_unitario), 2)

        execute(lambda: self.repository.alterar(item))
        self._recalcular_compra(item.compra_id)

        return self.repository.get_by_id(id)

    def deletar(self, id: int) -> None:
        item = self.repository.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de compra não encontrado.",
            )

        compra_id = item.compra_id
        execute(lambda: self.repository.deletar(item))
        self._recalcular_compra(compra_id)

