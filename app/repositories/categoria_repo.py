from sqlalchemy.orm import Session

from app.models.categoria import Categoria

class CategoriaRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_nome(self, nome: str) -> Categoria | None:
        return (
            self.db.query(Categoria)
            .filter(Categoria.nome == nome)
            .first()
        )

    def criar(self, categoria: Categoria) -> Categoria:
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)

        return categoria