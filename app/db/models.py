from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    wallet_id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[Decimal]
