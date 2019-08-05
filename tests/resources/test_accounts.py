import pytest

from arcus.resources import Account


@pytest.mark.vcr
def test_get_account_info(client):
    account = client.account
    assert type(account) is Account
    assert account.currency == 'MXN'
    assert type(account.balance) is float
    assert account.balance > account.minimum_balance


@pytest.mark.vcr
def test_get_account_info_proxy(client_proxy):
    account = client_proxy.account
    assert type(account) is Account
    assert account.currency == 'MXN'
    assert type(account.balance) is float
    assert account.balance > account.minimum_balance
