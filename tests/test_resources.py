import os

import pytest
import vcr

from arcus import Client
from arcus.exc import UnprocessableEntity
from arcus.resources import Account


ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']

ARCUS_CLIENT = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY, sandbox=True)


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_resources')
def test_get_account_info():
    client = ARCUS_CLIENT
    account = client.account
    assert type(account) is Account
    assert account.currency == 'MXN'
    assert type(account.balance) is float
    assert account.balance > account.minimum_balance


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_resources')
def test_topup():
    client = ARCUS_CLIENT
    biller_id = 13599
    account_number = '5599999999'
    amount = 100.0
    topup = client.topups.create(biller_id, account_number, amount)
    assert topup.biller_id == biller_id
    assert topup.account_number == account_number
    assert topup.bill_amount == amount
    assert topup.ending_balance < topup.starting_balance
    assert topup.chain_earned + topup.chain_paid == amount


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_resources')
def test_topup_invalid_phone_number():
    client = Client(ARCUS_API_KEY,
                    ARCUS_SECRET_KEY,
                    sandbox=True)
    biller_id = 13599
    account_number = '559999'
    amount = 100.0
    with pytest.raises(UnprocessableEntity) as excinfo:
        client.topups.create(biller_id, account_number, amount)
    exc = excinfo.value
    assert exc.code == 'R5'
    assert exc.message == 'Invalid Phone Number'
