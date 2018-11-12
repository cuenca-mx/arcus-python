import os

import pytest

from arcus import Client
from arcus.exc import InvalidAuth


API_KEY = os.environ['ARCUS_API_KEY']
SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


def test_valid_auth():
    client = Client(API_KEY, SECRET_KEY, sandbox=True)
    resp = client.get('account')
    assert resp.status_code == 200
    assert resp.data['currency'] == 'MXN'
    assert isinstance(resp.data['account_balance'], float)
    assert resp.data['account_balance'] > resp.data['minimum_balance']


def test_invalid_auth():
    # Attempt using sandbox creds on production API endpoint
    client = Client(API_KEY, SECRET_KEY)  # default is sandbox=False
    with pytest.raises(InvalidAuth) as excinfo:
        client.get('account')
    assert excinfo.value == 'Invalid API authentication credentials'
