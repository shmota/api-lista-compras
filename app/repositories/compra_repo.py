from sqlalchemy.orm import Query, Session

from app.models.compra import Compra


class CompraRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def criar(self, compra: Compra) -> Compra:
        self.db.add(compra)
        self.db.commit()
        self.db.refresh(compra)
        return compra

    def get_by_id(self, id: int) -> Compra | None:
        return self.db.get(Compra, id)

    def listar(self, *filtros) -> Query[Compra]:
        if not filtros:
            query = self.db.query(Compra)
        else:
            query = self.db.query(Compra).filter(*filtros)

        return query.order_by(Compra.data.desc(), Compra.id.desc())

    def alterar(self, compra: Compra) -> Compra:
        self.db.merge(compra)
        self.db.commit()
        return self.get_by_id(compra.id)

    def deletar(self, compra: Compra) -> None:
        self.db.delete(compra)
        self.db.commit()
