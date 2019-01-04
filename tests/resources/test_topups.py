import pytest
import vcr

from arcus.exc import UnprocessableEntity

from ..fixtures import client


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_topups')
def test_topup(client):
    biller_id = 13599
    account_number = '5599999999'
    amount = 100.0
    topup = client.topups.create(biller_id, account_number, amount)
    assert topup.biller_id == biller_id
    assert topup.account_number == account_number
    assert topup.bill_amount == amount
    assert topup.ending_balance < topup.starting_balance
    assert topup.chain_earned + topup.chain_paid == amount


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_topups')
def test_topup_invalid_phone_number(client):
    biller_id = 13599
    account_number = '559999'
    amount = 100.0
    with pytest.raises(UnprocessableEntity) as excinfo:
        client.topups.create(biller_id, account_number, amount)
    exc = excinfo.value
    assert exc.code == 'R5'
    assert exc.message == 'Invalid Phone Number'


def test_topup_list(client):
    with pytest.raises(NotImplementedError):
        client.topups.list()
