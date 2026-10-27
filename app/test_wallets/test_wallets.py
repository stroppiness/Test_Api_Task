from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from api.service.exceptions import (InsufficientFundsError, InvalidAmountError,
                                    WalletAlreadyExistsError,
                                    WalletNotFoundError, WalletSaveError)
from api.v1 import wallet as wallet_module


@pytest.mark.asyncio
async def test_create_wallet(client, monkeypatch):
    '''Тест для проверки ручки создания кошелька'''
    wallet_uuid = uuid4()

    mock = AsyncMock()

    monkeypatch.setattr(
        wallet_module,
        'create_new_wallet',
        mock,
    )

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/create'
    )

    assert response.status_code == 201
    assert response.json() == 'Success'

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_wallet_already_exists(client, monkeypatch):
    '''Тест для проверки исключения WalletAlreadyExist создания кошелька'''
    wallet_uuid = uuid4()

    mock = AsyncMock()
    mock.side_effect = WalletAlreadyExistsError()

    monkeypatch.setattr(
        wallet_module,
        'create_new_wallet',
        mock,
    )

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/create'
    )

    assert response.status_code == 409
    assert response.json()['detail'] == 'Кошелёк уже существует'

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_wallet_wrong_uuid(client, monkeypatch):
    '''Тест для проверки исключения ValueError в ручке создания кошелька'''
    wallet_uuid = uuid4()

    mock = AsyncMock()
    mock.side_effect = ValueError()

    monkeypatch.setattr(
        wallet_module,
        'create_new_wallet',
        mock,
    )

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/create'
    )

    assert response.status_code == 400
    assert response.json()['detail'] == 'Некорректный формат UUID'

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_wallet_server_error(client, monkeypatch):
    '''Тест для проверки исключения WalletSaveError
    в ручке создания кошелька
    '''
    wallet_uuid = uuid4()

    mock = AsyncMock()
    mock.side_effect = WalletSaveError()

    monkeypatch.setattr(
        wallet_module,
        'create_new_wallet',
        mock,
    )

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/create'
    )

    assert response.status_code == 500
    assert response.json()['detail'] == 'Ошибка добавления кошелька'

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_income_or_expence(client, monkeypatch):
    '''Тест для проверки ручки пополнения или снятия денег'''
    wallet_uuid = uuid4()

    mock = AsyncMock(return_value=Decimal(12))

    monkeypatch.setattr(
        wallet_module,
        'add_or_remove_money',
        mock,
    )

    payload = {'operation_type': 'DEPOSIT', 'amount': 12}

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json=payload
    )

    assert response.status_code == 200
    assert response.json() == '12'

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_income_or_expence_wallet_not_found(client, monkeypatch):
    '''Тест для проверки исключения WalletNotFoundError
    в ручке пополнения или снятия денег
    '''
    wallet_uuid = uuid4()

    mock = AsyncMock()
    mock.side_effect = WalletNotFoundError

    monkeypatch.setattr(
        wallet_module,
        'add_or_remove_money',
        mock,
    )

    payload = {'operation_type': 'DEPOSIT', 'amount': 12}

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json=payload
    )

    assert response.status_code == 404
    assert response.json()['detail'] == f'Кошелек с ID {wallet_uuid} не найден'

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_income_or_expence_invalid_amount(client, monkeypatch):
    '''Тест для проверки исключения InvalidAmountError
    в ручке пополнения или снятия денег
    '''
    wallet_uuid = uuid4()

    mock = AsyncMock()
    mock.side_effect = InvalidAmountError()

    monkeypatch.setattr(
        wallet_module,
        'add_or_remove_money',
        mock,
    )

    payload = {'operation_type': 'DEPOSIT', 'amount': 12}

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json=payload
    )

    assert response.status_code == 400
    assert response.json()['detail'] == ('Сумма пополнения должна '
                                         'быть больше нуля')

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_income_or_expence_not_enough_money(client, monkeypatch):
    '''Тест для проверки исключения InsufficientFundsError
    в ручке пополнения или снятия денег
    '''
    wallet_uuid = uuid4()

    mock = AsyncMock()
    mock.side_effect = InsufficientFundsError()

    monkeypatch.setattr(
        wallet_module,
        'add_or_remove_money',
        mock,
    )

    payload = {'operation_type': 'DEPOSIT', 'amount': 12}

    response = await client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json=payload
    )

    assert response.status_code == 422
    assert response.json()['detail'] == ('Недостаточно средств на счёте')

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_balance(client, monkeypatch):
    '''Тест для проверки ручки получения баланса'''
    wallet_uuid = uuid4()

    mock = AsyncMock(return_value=Decimal(12))

    monkeypatch.setattr(
        wallet_module,
        'get_wallet_balance',
        mock,
    )

    response = await client.get(f'/api/v1/wallets/{wallet_uuid}')

    assert response.status_code == 200
    assert response.json() == '12'

    mock.assert_awaited_once()


@pytest.mark.asyncio
async def get_balance_wallet_not_found(client, monkeypatch):
    '''Тест для проверки исключения WalletNotFoundError
    в ручке получения баланса
    '''
    wallet_uuid = uuid4()

    mock = AsyncMock()
    mock.side_effect = WalletNotFoundError()

    monkeypatch.setattr(
        wallet_module,
        'add_or_remove_money',
        mock,
    )

    response = await client.post(f'/api/v1/wallets/{wallet_uuid}/operation')

    assert response.status_code == 404
    assert response.json()['detail'] == ('Кошелёк не существует')

    mock.assert_awaited_once()
