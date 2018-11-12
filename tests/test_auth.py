import os

import pytest


from arcus import Client
import exc

API_KEY = os.environ['ARCUS_API_KEY']
SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


def test_valid_auth():
    client = Client(API_KEY, SECRET_KEY, sandbox=True)
    account = client.get('account')
    assert type(account) is dict
    assert account['currency'] == 'MXN'
    assert type(account['balance']) is float
    assert account['balance'] > account['minimum_balance']


def test_invalid_auth():
    client = Client(API_KEY, SECRET_KEY)  # default is sandbox=False

    with pytest.raises(exc.InvalidAuth) as excinfo:
        client.get('account')
    assert excinfo.value.value == 'Invalid API authentication credentials'
