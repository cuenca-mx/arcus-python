import os

import pytest

from arcus.client import Client
from arcus.exc import InvalidAuth

ARCUS_API_KEY = os.environ['ARCUS_API_KEY']
ARCUS_SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


@pytest.mark.vcr
def test_valid_auth():
    client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY, sandbox=True)
    account = client.get('/account')
    assert type(account) is dict
    assert account['currency'] == 'MXN'
    assert type(account['balance']) is float
    assert account['balance'] > account['minimum_balance']


@pytest.mark.vcr
def test_invalid_auth():
    # default is sandbox=False
    client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY)
    with pytest.raises(InvalidAuth):
        client.get('/account')


@pytest.mark.vcr
def test_valid_auth_post():
    data = dict(biller_id=40, account_number='501000000007')
    client = Client(ARCUS_API_KEY, ARCUS_SECRET_KEY, sandbox=True)
    bill = client.post('/bills', data)
    assert type(bill) is dict
    assert bill['biller_id'] == 40
    assert bill['account_number'] == '501000000007'
    assert type(bill['balance']) is float
