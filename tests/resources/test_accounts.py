import pytest

from arcus.exc import Forbidden
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


@pytest.mark.vcr
def test_post_method_proxy(client_proxy):
    with pytest.raises(Forbidden):
        client_proxy.post('/account', {})
