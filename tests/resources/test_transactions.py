import pytest

from arcus.resources import Transaction


@pytest.mark.vcr
def test_transactions_list(client):
    transactions = client.transactions.list()
    assert transactions
    assert type(transactions) is list
    assert all(isinstance(txn, Transaction) for txn in transactions)
