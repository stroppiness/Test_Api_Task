from decimal import Decimal
from uuid import UUID

from api.repository.wallet import (create_wallet_by_id, get_wallet_by_id,
                                   save_wallet)
from api.schemas.schemas import WalletOperations
from api.service.exceptions import (InsufficientFundsError, InvalidAmountError,
                                    WalletAlreadyExistsError,
                                    WalletNotFoundError, WalletSaveError)
from db.database import SessionDep
from db.models import Wallet
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


async def create_new_wallet(wallet_id: UUID, db: SessionDep) -> Wallet:
    try:
        return await create_wallet_by_id(wallet_id, db)

    except IntegrityError:
        raise WalletAlreadyExistsError

    except SQLAlchemyError:
        raise WalletSaveError


async def get_wallet_balance(wallet_id: UUID, db: SessionDep) -> Decimal:
    wallet = await get_wallet_by_id(wallet_id, db)

    if not wallet:
        raise WalletNotFoundError

    balance = wallet.balance

    return balance


async def add_or_remove_money(
    wallet_id: UUID,
    payload: WalletOperations,
    db: SessionDep
) -> Decimal:
    amount = payload.amount
    if amount <= 0:
        raise InvalidAmountError

    wallet = await get_wallet_by_id(wallet_id, db)

    if not wallet:
        raise WalletNotFoundError

    if payload.operation_type == 'DEPOSIT':
        wallet.balance += amount
        await save_wallet(wallet, db)
        return wallet.balance

    if payload.operation_type == 'WITHDRAW':
        if wallet.balance < amount:
            raise InsufficientFundsError('Недостаточно средств на счёте')

        wallet.balance -= amount
        await save_wallet(wallet, db)
        return wallet.balance
