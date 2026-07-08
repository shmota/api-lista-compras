from sqlalchemy.orm import Session

from app.models.categoria import Categoria

class CategoriaRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_nome(self, nome: str) -> Categoria | None:
        return (
            self.listar(Categoria.nome == nome).first()
        )

    def listar(self, filtros: dict = {}) -> list[Categoria]:
        
        if not filtros:
            return self.db.query(Categoria)
        else:
            return self.db.query(Categoria).filter_by(**filtros)
        
    def criar(self, categoria: Categoria) -> Categoria:
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)

        return categoria
    