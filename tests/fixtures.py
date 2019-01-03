import pytest

from arcus import Client


@pytest.fixture()
def client():
    yield Client(sandbox=True)
