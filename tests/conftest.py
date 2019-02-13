import pytest

from botmaker import Client


@pytest.fixture(scope='module')
def vcr_config():
    config = dict()
    # Replace the Authorization request header with 'DUMMY' in cassettes
    config['filter_headers'] = [('access-token', 'DUMMY')]
    config['filter_post_data_parameters'] = [
        ('chatChannelNumber', '5215500000000'),
        ('platformContactId', '5215522222222'),
        ('contacts', ['+55 1 55 1234 5678'])
    ]
    return config


@pytest.fixture
def client():
    # Using BOTMAKER_ACCESS_TOKEN from env
    yield Client()
