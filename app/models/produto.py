from sqlalchemy import ForeignKey, func, DateTime, CheckConstraint, text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from app.core.database import Base


class Produto(Base):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(
        autoincrement=True, 
        primary_key=True,
        index=True
    )
    nome: Mapped[str] = mapped_column(
        unique=True, 
        nullable=False
    )
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria.id"),
        nullable=False
    )
    unidade_medida_id: Mapped[int] = mapped_column(
        ForeignKey("unidade_medida.id"),        
        nullable=False
    )
    quantidade_atual: Mapped[float] = mapped_column(
        Numeric(12, 3),
        CheckConstraint("quantidade_atual >= 0"),
        nullable=False,
        server_default=text("0")
    )
    quantidade_ideal: Mapped[float] = mapped_column(
        Numeric(12, 3),
        CheckConstraint("quantidade_ideal >= 0"),
        nullable=False,
        server_default=text("0"),
    )
    observacao: Mapped[str] = mapped_column(
        server_default=text("''"),
    )
    ativo: Mapped[bool] = mapped_column(
        nullable=False,
        server_default=text("TRUE")
    )
    criado_em: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )
    atualizado_em: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )
    
    categoria = relationship(
        "Categoria",
        back_populates="produtos"
    )

    unidade_medida = relationship(
        "UnidadeMedida"
    )
    
    @property
    def categoria_nome(self):
        return self.categoria.nome

    @property
    def unidade_medida_nome(self):
        return self.unidade_medida.nome