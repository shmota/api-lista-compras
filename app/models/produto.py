from sqlalchemy import ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
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
    quantidade_atual: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )
    quantidade_ideal: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )
    observacao: Mapped[str] = mapped_column(
        default=""
    )
    ativo: Mapped[bool] = mapped_column(
        nullable=False,
        default=True
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
    