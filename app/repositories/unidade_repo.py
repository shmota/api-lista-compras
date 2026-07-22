from sqlalchemy.orm import Session

from app.models.unidade_medida import UnidadeMedida

class UnidadeRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, id: str) -> UnidadeMedida:
        return self.db.get(UnidadeMedida, id)
        
    def existe_nome(self, nome: str) -> UnidadeMedida:
        return self.db.query(UnidadeMedida).filter(UnidadeMedida.nome.ilike(nome)).first() is not None
    
    
    def existe_sigla(self, sigla: str) -> bool:
        return self.db.query(UnidadeMedida).filter(UnidadeMedida.sigla.like(sigla)).first() is not None
        
    def criar(self, unidade: UnidadeMedida) -> UnidadeMedida:
        self.db.add(unidade)
        self.db.commit()
        self.db.refresh(unidade)

        return unidade
    
    def listar(self, *filtros) -> Query[UnidadeMedida]:
        
        if filtros is None:
            linhas = self.db.query(UnidadeMedida)
        else:
            linhas = self.db.query(UnidadeMedida).filter(*filtros)
            
        linhas = linhas.order_by(UnidadeMedida.id.asc())
        
        return linhas
    
    def alterar(self, dados: UnidadeMedida) -> UnidadeMedida:
        
        unidade = self.get_by_id(dados.id)
        
        unidade.sigla = dados.sigla
        unidade.nome = dados.nome
        
        self.db.commit()
        self.db.refresh(unidade)

        return unidade
    
    def deletar(self, unidade: UnidadeMedida) -> None:
        self.db.delete(unidade)
        self.db.commit()