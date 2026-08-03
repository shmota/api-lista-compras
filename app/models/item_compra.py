import datetime
import decimal
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ItemCompra(Base):
    __tablename__ = "item_compra"

    id: Mapped[int] = mapped_column(
        autoincrement=True, 
        primary_key=True,
        index=True
    )
    compra_id: Mapped[int] = mapped_column(
        ForeignKey("compra.id", ondelete="CASCADE"),
        nullable=False
    )
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produto.id"),
        nullable=False
    )
    quantidade: Mapped[float] = mapped_column(
        Numeric(12, 3),
        CheckConstraint("quantidade >= 0"),
        nullable=False,
        server_default=text("0")
    )
    valor_unitario: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2),
        CheckConstraint("valor_unitario >= 0"),
        nullable=False,
        server_default=text("0")
    )
    valor_total: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2),
        CheckConstraint("valor_total >= 0"),
        nullable=False,
        server_default=text("0")
    )

    compra = relationship(
        "Compra",
        back_populates="itens"
    )

    produto = relationship(
        "Produto"
    )