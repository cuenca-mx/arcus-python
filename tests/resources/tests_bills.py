import pytest
import vcr

from arcus import exc
from arcus.resources import Bill

from ..fixtures import client


@vcr.use_cassette(cassette_library_dir='tests/cassettes/resources/test_bills')
def test_create_bill(client):
    bill = client.bills.create(40, '501000000007')
    assert type(bill) is Bill
    assert bill.biller_id == 40
    assert bill.account_number == '501000000007'
    assert type(bill.balance) is float


@vcr.use_cassette(cassette_library_dir='tests/cassettes/resources/test_bills')
def test_invalid_biller_id(client):
    invalid_biller_id = 99999999
    with pytest.raises(exc.InvalidBiller):
        client.bills.create(invalid_biller_id, '1234')


@vcr.use_cassette(cassette_library_dir='tests/cassettes/resources/test_bills')
def test_invalid_account_number(client):
    invalid_account_number  = '501000000004'
    with pytest.raises(exc.InvalidAccountNumber) as excinfo:
        client.bills.create(40, invalid_account_number)


@vcr.use_cassette(cassette_library_dir='tests/cassettes/resources/test_bills')
def test_successful_payment(client):
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    transaction = bill.pay()
    assert transaction.id
    assert transaction.status == 'fulfilled'
