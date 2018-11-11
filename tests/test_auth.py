import os

import pytest

import arcus
from arcus.exc import InvalidAuth


API_KEY = os.environ['ARCUS_API_KEY']
SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


def test_valid_auth():
    arcus.configure(API_KEY, SECRET_KEY, sandbox=True)
    resp = arcus.get('/account')
    assert resp.status_code == 200
    assert resp.data['currency'] == 'MXN'
    assert isinstance(resp.data['account_balance'], float)
    assert resp.data['account_balance'] > resp.data['minimum_balance']


def test_invalid_auth():
    with pytest.raises(InvalidAuth) as excinfo:
        arcus.get('/account')
    assert excinfo.value == 'API credentials have not been configured'

    # Attempt using sandbox creds on production API endpoint
    arcus.configure(API_KEY, SECRET_KEY)  # default is sandbox=False
    with pytest.raises(InvalidAuth) as excinfo:
        arcus.get('/account')
    assert excinfo.value == 'Invalid API authentication credentials'
