from sqlalchemy.orm import Session

from app.models.produto import Produto

class ProdutoRepository:
    
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def existe_nome(self, nome: str) -> bool:
        return self.db.query(Produto).filter(Produto.nome.ilike(nome)).first() != None
        
    def criar(self, produto: Produto) -> Produto:        
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        
        return produto
    
    def get_by_id(self, id: int) -> Produto:
        return self.db.get(Produto, id)
    
    def listar(self, *filtros) -> Query[Produto]:
        
        if filtros is None:
            linhas = self.db.query(Produto)
            
        else:
            linhas = self.db.query(Produto).filter(*filtros)
            
        linhas = linhas.order_by(Produto.id.asc())
        
        return linhas
    
    def alterar(self, produto: Produto) -> Produto:
        
        self.db.merge(produto)
        
        self.db.commit()
        
        return self.get_by_id(produto.id)

    def deletar(self, produto: Produto) -> None:
        self.db.delete(produto)
        self.db.commit()