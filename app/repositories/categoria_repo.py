from sqlalchemy.orm import Session

from app.models.categoria import Categoria

class CategoriaRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, id: int):
        return self.db.get(Categoria, id)
        
    def existe_nome(self, nome: str) -> Categoria:
        return self.db.query(Categoria).filter(Categoria.nome.ilike(nome)).first() is not None

    def listar(self, *filtros) -> Query[Categoria]:
        
        if filtros is None:
            linhas = self.db.query(Categoria)
        else:
            linhas = self.db.query(Categoria).filter(*filtros)
            
        linhas = linhas.order_by(Categoria.id.asc())
        
        return linhas
        
    def criar(self, categoria: Categoria) -> Categoria:
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)

        return categoria
    
    def alterar(self, dados: Categoria) -> Categoria:
        
        categoria = self.db.get(Categoria, dados.id)
        
        categoria.nome = dados.nome
        
        self.db.commit()
        self.db.refresh(categoria)

        return categoria
    
    def deletar(self, categoria: Categoria) -> None:
        self.db.delete(categoria)
        self.db.commit()