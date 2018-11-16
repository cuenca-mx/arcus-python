import os

import pytest

from arcus import Client
from arcus.exc import UnprocessableEntity
from arcus.resources import Account, Bill


ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']

ARCUS_CLIENT = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY, sandbox=True)


def test_get_account_info():
    client = ARCUS_CLIENT
    account = client.account
    assert type(account) is Account
    assert account.currency == 'MXN'
    assert type(account.balance) is float
    assert account.balance > account.minimum_balance


def test_create_bill():
    client = ARCUS_CLIENT
    bill = client.bills.create(40, '501000000007')
    assert type(bill) is Bill
    assert bill.biller_id == 40
    assert bill.account_number == '501000000007'
    assert type(bill.balance) is float


def test_create_bill_wrong_account_number():
    client = ARCUS_CLIENT
    with pytest.raises(UnprocessableEntity) as excinfo:
        client.bills.create(40, '501000000004')
    ex = excinfo.value
    assert ex.code == 'R2'
    assert ex.message == 'Invalid Account Number'


def test_successful_payment():
    client = ARCUS_CLIENT
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    transaction = bill.pay()
    assert transaction.id
    assert transaction.status == 'fulfilled'


def test_unexpected_error():
    arcus = ARCUS_CLIENT
    with pytest.raises(Exception) as excinfo:
        arcus.bills.create(6900, '1111362009')
    exc = excinfo.value
    assert exc.code == 'R9'
    assert exc.message.startswith('Unexpected error')


def test_cancel_bill():
    client = ARCUS_CLIENT
    bill = client.bills.create(35, '123456851236')
    transaction = bill.pay(bill.balance)
    cancellation = client.transactions.cancel(transaction.id)
    assert cancellation.code == 'R0'
    assert cancellation.message == 'Transaction successful'

    updated_transaction = client.transactions.get(transaction.id)
    assert updated_transaction.id == transaction.id
    assert updated_transaction.status == 'refunded'


def test_consult_error():
    client = ARCUS_CLIENT
    with pytest.raises(UnprocessableEntity) as excinfo:
        client.bills.create(2901, '1111322016')
    exc = excinfo.value
    assert exc.code == 'R16'
    assert exc.message == 'Failed to make the consult, please try again later'


def test_biller_maintenance():
    client = ARCUS_CLIENT
    with pytest.raises(UnprocessableEntity) as excinfo:
        client.bills.create(1821, '1111992022')
    exc = excinfo.value
    assert exc.code == 'R22'
    assert exc.message == (
        'Biller maintenance in progress, please try again later')


def test_timeout_on_payment():
    client = ARCUS_CLIENT
    bill = client.bills.create(37, '2424240024')
    with pytest.raises(UnprocessableEntity) as excinfo:
        bill.pay()
    exc = excinfo.value
    assert exc.code == 'R24'
    assert exc.message == 'Timeout from biller'
