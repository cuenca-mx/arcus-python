import vcr

from arcus.resources import Transaction

from ..fixtures import client


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_transactions')
def test_transactions_list(client):
    transactions = client.transactions.list()
    assert transactions
    assert type(transactions) is list
    assert all(isinstance(txn, Transaction) for txn in transactions)
