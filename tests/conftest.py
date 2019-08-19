import pytest
import requests_mock

from arcus import Client


@pytest.fixture
def client():
    yield Client(sandbox=True)


@pytest.fixture
def client_proxy():
    with requests_mock.mock() as m:
        m.get('http://127.0.0.1:3001/account', json=dict(
            name='Cuenca',
            balance=60454.43,
            minimum_balance=0.0,
            currency='MXN'
        )
        )
        m.post(
            'http://127.0.0.1:3001/account',
            json=dict(
                message='Missing Authentication Token'
            ),
            status_code=403
        )
        yield Client(sandbox=True, proxy='http://127.0.0.1:3001')
