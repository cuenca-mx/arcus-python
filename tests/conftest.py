import pytest

from arcus import Client


@pytest.fixture
def client():
    yield Client(sandbox=True)


@pytest.fixture
def client_proxy():
    yield Client(sandbox=True, proxy='http://127.0.0.1:3001')
