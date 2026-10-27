from decimal import Decimal
from uuid import UUID, uuid4

from db.database import Base
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column


class Wallet(Base):
    __tablename__ = 'wallets'

    wallet_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    balance: Mapped[Decimal]
