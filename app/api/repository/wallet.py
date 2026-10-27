from uuid import UUID

from db.database import SessionDep
from db.models import Wallet
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


async def create_wallet_by_id(wallet_id: UUID, db: SessionDep) -> Wallet:
    wallet = Wallet(wallet_id=wallet_id, balance=0)
    db.add(wallet)
    try:
        await db.commit()
        await db.refresh(wallet)
        return wallet

    except IntegrityError:
        await db.rollback()
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise


async def get_wallet_by_id(wallet_id: UUID, db: SessionDep) -> Wallet | None:
    query = select(Wallet).where(
        Wallet.wallet_id == wallet_id).with_for_update()
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def save_wallet(wallet: Wallet, db: SessionDep) -> Wallet:
    try:
        await db.commit()
        await db.refresh(wallet)
        return True

    except SQLAlchemyError:
        await db.rollback()
        raise
    return wallet
