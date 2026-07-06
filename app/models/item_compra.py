from sqlalchemy import ForeignKey, func, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime
import decimal

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
    quantidade: Mapped[int] = mapped_column(
        CheckConstraint("quantidade >= 0"),
        nullable=False,
        default=0
    )
    valor_unitario: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2),
        CheckConstraint("valor_unitario >= 0"),
        nullable=False,
        default=0
    )
    valor_total: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2),
        CheckConstraint("valor_total >= 0"),
        nullable=False,
        default=0
    )
    