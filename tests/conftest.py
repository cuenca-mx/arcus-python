import os

import pytest
import requests_mock

from arcus import Client

PROXY = os.environ['ARCUS_PROXY']


@pytest.fixture
def client():
    yield Client(sandbox=True)


@pytest.fixture
def client_proxy():
    with requests_mock.mock() as m:
        m.get(f'{PROXY}/account', json=dict(
            name='Cuenca',
            balance=60454.43,
            minimum_balance=0.0,
            currency='MXN'
        )
        )
        m.post(
            f'{PROXY}/account',
            json=dict(
                message='Missing Authentication Token'
            ),
            status_code=403
        )
        yield Client(sandbox=True, proxy=PROXY)
