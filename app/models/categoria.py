from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(
        autoincrement=True, 
        primary_key=True,
        index=True
    )
    nome: Mapped[str] = mapped_column(
        unique=True, 
        nullable=False,
        index=True
    )