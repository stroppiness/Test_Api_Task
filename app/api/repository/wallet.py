#ЗАПРОСЫ В БД ЧЕРЕЗ SQLALCHEMY
import os

from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from db.database import SessionDep
from db.models import Wallet


async def create_wallet_by_id(wallet_id: int, db: SessionDep) -> Wallet:
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


async def get_wallet_by_id(wallet_id: int, db: SessionDep) -> Wallet | None:
    query = select(Wallet).where(Wallet.wallet_id == wallet_id).with_for_update()
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def add_amount(wallet_id):
    pass


async def save_wallet(wallet: Wallet, db: SessionDep) -> Wallet:
    try:
        await db.commit()
        await db.refresh(wallet)
        return True

    except SQLAlchemyError:
        await db.rollback()
        raise
    return wallet
