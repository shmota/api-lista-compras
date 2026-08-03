from sqlalchemy.orm import Query, Session

from app.models.item_compra import ItemCompra


class ItemCompraRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def criar(self, item: ItemCompra) -> ItemCompra:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_id(self, id: int) -> ItemCompra | None:
        return self.db.get(ItemCompra, id)

    def listar(self, *filtros) -> Query[ItemCompra]:
        if not filtros:
            query = self.db.query(ItemCompra)
        else:
            query = self.db.query(ItemCompra).filter(*filtros)

        return query.order_by(ItemCompra.id.asc())

    def alterar(self, item: ItemCompra) -> ItemCompra:
        self.db.merge(item)
        self.db.commit()
        return self.get_by_id(item.id)

    def deletar(self, item: ItemCompra) -> None:
        self.db.delete(item)
        self.db.commit()
