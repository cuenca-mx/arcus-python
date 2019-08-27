import pytest
from unittest.mock import patch

from arcus import Client
from arcus.exc import Forbidden
from arcus.resources import Account


@pytest.mark.vcr
def test_get_account_info(client):
    accounts = client.accounts
    assert type(accounts) is dict
    assert set(accounts.keys()) == {'primary', 'topup'}
    for account in accounts.values():
        assert type(account) is Account
        assert account.currency == 'MXN'
        assert type(account.balance) is float
        assert account.balance > account.minimum_balance


def test_get_account_info_proxy(client_proxy):
    accounts = client_proxy.accounts
    assert type(accounts) is dict
    assert set(accounts.keys()) == {'primary'}
    for account in accounts.values():
        assert type(account) is Account
        assert account.currency == 'MXN'
        assert type(account.balance) is float
        assert account.balance > account.minimum_balance


def test_post_method_proxy(client_proxy):
    with pytest.raises(Forbidden):
        client_proxy.post('/account', {})


@patch.dict('os.environ', {'ARCUS_PROXY': ''})
def test_get_account_info_without_proxy():
    client_without_proxy = Client(sandbox=True)
    accounts = client_without_proxy.accounts
    assert type(accounts) is dict
    assert set(accounts.keys()) == {'primary', 'topup'}
    for account in accounts.values():
        assert type(account) is Account
        assert account.currency == 'MXN'
        assert type(account.balance) is float
        assert account.balance > account.minimum_balance
