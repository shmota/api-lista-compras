from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class UnidadeMedida(Base):
    __tablename__ = "unidade_medida"

    id: Mapped[int] = mapped_column(
        autoincrement=True, 
        primary_key=True,
        index=True
    )
    nome: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    sigla: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )