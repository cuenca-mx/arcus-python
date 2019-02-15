import pytest

from arcus import Client


@pytest.fixture(scope='module')
def vcr_config():
    config = dict()
    # Replace the Authorization request header with 'DUMMY' in cassettes
    config['filter_headers'] = [('Authorization:', 'DUMMY')]
    return config


@pytest.fixture
def client():
    yield Client(sandbox=True)
