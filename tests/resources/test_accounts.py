import vcr

from arcus.resources import Account

from ..fixtures import client


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_accounts')
def test_get_account_info(client):
    account = client.account
    assert type(account) is Account
    assert account.currency == 'MXN'
    assert type(account.balance) is float
    assert account.balance > account.minimum_balance
