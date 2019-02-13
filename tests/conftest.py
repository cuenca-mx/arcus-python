import pytest

from arcus import Client


@pytest.fixture(scope='module')
def vcr_config():
    config = dict()
    # Replace the Authorization request header with 'DUMMY' in cassettes
    config['filter_headers'] = [('Authorization:', 'DUMMY')]
    config['filter_auth_post_parameters'] = [
        ('biller_id', '40'),
        ('account_number', '501000000007')
    ]
    return config


@pytest.fixture
def client():
    #
    yield Client()

