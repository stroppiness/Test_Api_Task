from decimal import Decimal
from uuid import UUID

from api.schemas.schemas import WalletOperations
from api.service.exceptions import (InsufficientFundsError, InvalidAmountError,
                                    WalletAlreadyExistsError,
                                    WalletNotFoundError, WalletSaveError)
from api.service.wallet import (add_or_remove_money, create_new_wallet,
                                get_wallet_balance)
from db.database import SessionDep
from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

router = APIRouter()


@router.post('/{wallet_uuid}/create', status_code=status.HTTP_201_CREATED)
async def create_wallet(wallet_uuid: UUID, db: SessionDep) -> str:
    try:
        await create_new_wallet(wallet_uuid, db)
        return ('Success')

    except (ValidationError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Некорректный формат UUID'
        )

    except WalletAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Кошелёк уже существует'
        )

    except WalletSaveError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка добавления кошелька'
        )


@router.post(
    '/{wallet_uuid}/operation', status_code=status.HTTP_200_OK)
async def income_or_expence(
    wallet_uuid: UUID,
    payload: WalletOperations,
    db: SessionDep
) -> Decimal:
    try:
        return await add_or_remove_money(wallet_uuid, payload, db)

    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(f'Кошелек с ID {wallet_uuid} не найден')
        )

    except InvalidAmountError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=('Сумма пополнения должна быть больше нуля')
        )

    except InsufficientFundsError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=('Недостаточно средств на счёте')
        )


@router.get('/{wallet_uuid}', status_code=status.HTTP_200_OK)
async def get_balance(wallet_uuid: UUID, db: SessionDep) -> Decimal:
    try:
        return await get_wallet_balance(wallet_uuid, db)

    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Кошелёк не существует'
        )
