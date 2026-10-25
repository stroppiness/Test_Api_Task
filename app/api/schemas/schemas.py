from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class WalletOperations(BaseModel):
    operation_type: Literal['DEPOSIT', 'WITHDRAW'] = Field(
        ...,
        examples=['DEPOSIT or WITHDRAW'],
    )
    amount: Decimal = Field(
        ...,
        gt=0,
        description='Сумма должна быть больше 0',
    )
