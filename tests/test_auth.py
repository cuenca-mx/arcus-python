import os

import pytest

from arcus.exc import InvalidAuth
from arcus.client import Client


API_KEY = os.environ['ARCUS_API_KEY']
SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


def test_valid_auth():
    client = Client(API_KEY, SECRET_KEY, sandbox=True)
    account = client.get('/account')
    assert type(account) is dict
    assert account['currency'] == 'MXN'
    assert type(account['balance']) is float
    assert account['balance'] > account['minimum_balance']


def test_invalid_auth():
    client = Client(API_KEY, SECRET_KEY)  # default is sandbox=False

    with pytest.raises(InvalidAuth) as excinfo:
        client.get('/account')
    assert excinfo.value.value == 'Invalid API authentication credentials'


def test_valid_auth_post():
    data = dict(biller_id=40, account_number='501000000007')
    client = Client(API_KEY, SECRET_KEY, sandbox=True)
    bill = client.post('/bills', data)
    assert type(bill) is dict
    assert bill['biller_id'] == 40
    assert bill['account_number'] == '501000000007'
    assert type(bill['balance']) is float
