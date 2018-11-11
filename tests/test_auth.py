import os

import arcus


API_KEY = os.environ['ARCUS_API_KEY']
SECRET_KEY = os.environ['ARCUS_SECRET_KEY']


def test_auth():
    arcus.configure(API_KEY, SECRET_KEY, sandbox=True)
    resp = arcus.get('/account')
    assert resp.status_code == 200
    assert resp.data['currency'] == 'MXN'
    assert isinstance(resp.data['account_balance'], float)
    assert resp.data['account_balance'] > resp.data['minimum_balance']

