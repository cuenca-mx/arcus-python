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
    # import ipdb; ipdb.set_trace()


def test_create_bill_wrong_account_number():
    client = ARCUS_CLIENT
    with pytest.raises(UnprocessableEntity) as excinfo:
        client.bills.create(40, '501000000004')
    ex = excinfo.value
    assert ex.code == 'R2'
    assert ex.message == 'Invalid Account Number'


def test_unexpected_error():
    arcus = ARCUS_CLIENT
    with pytest.raises(Exception) as excinfo:
        arcus.bills.create(6900, '1111362009')
    exc = excinfo.value
    assert exc.code == 'R9'
    assert exc.message.startswith('Unexpected error')


def test_successful_payment():
    client = ARCUS_CLIENT
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    transaction = bill.pay()
    assert transaction.id
    assert transaction.status == 'fulfilled'


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
