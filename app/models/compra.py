from sqlalchemy import ForeignKey, func, Numeric, CheckConstraint, DateTime, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime
import decimal

from app.core.database import Base


class Compra(Base):
    __tablename__ = "compra"

    id: Mapped[int] = mapped_column(
        autoincrement=True, 
        primary_key=True,
        index=True
    )
    data: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )
    valor_total: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2),
        CheckConstraint("valor_total >= 0"),
        nullable=False,
        server_default=text("0")
    )
    creado_em: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )
    