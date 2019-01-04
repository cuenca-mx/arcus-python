import pytest
import vcr

from arcus import exc
from arcus.resources import Bill

from ..fixtures import client


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_create_bill(client):
    bill = client.bills.create(40, '501000000007')
    assert type(bill) is Bill
    assert bill.biller_id == 40
    assert bill.account_number == '501000000007'
    assert type(bill.balance) is float
    assert str(bill)
    assert repr(bill)


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_invalid_biller_id(client):
    invalid_biller_id = 99999999
    with pytest.raises(exc.InvalidBiller):
        client.bills.create(invalid_biller_id, '1234')


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_invalid_account_number(client):
    invalid_account_number = '501000000004'
    with pytest.raises(exc.InvalidAccountNumber):
        client.bills.create(40, invalid_account_number)


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_successful_payment(client):
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    transaction = bill.pay()
    assert transaction.id
    assert transaction.status == 'fulfilled'


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_unexpected_error(client):
    with pytest.raises(exc.UnprocessableEntity) as excinfo:
        client.bills.create(6900, '1111362009')
    e = excinfo.value
    assert e.code == 'R9'


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_cancel_bill(client):
    bill = client.bills.create(35, '123456851236')
    transaction = bill.pay(bill.balance)
    cancellation = transaction.cancel()
    assert cancellation['code'] == 'R0'
    assert cancellation['message'] == 'Transaction successful'

    updated_transaction = client.transactions.get(transaction.id)
    assert updated_transaction.id == transaction.id
    assert updated_transaction.status == 'refunded'


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_consult_error(client):
    with pytest.raises(exc.UnprocessableEntity) as excinfo:
        client.bills.create(2901, '1111322016')
    e = excinfo.value
    assert repr(e)
    assert e.code == 'R16'
    assert e.message == 'Failed to make the consult, please try again later'


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_biller_maintenance(client):
    with pytest.raises(exc.UnprocessableEntity) as excinfo:
        client.bills.create(1821, '1111992022')
    e = excinfo.value
    assert e.code == 'R22'
    assert e.message == (
        'Biller maintenance in progress, please try again later')


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_timeout_on_payment(client):
    bill = client.bills.create(37, '2424240024')
    with pytest.raises(exc.UnprocessableEntity) as excinfo:
        bill.pay()
    e = excinfo.value
    assert e.code == 'R24'
    assert e.message == 'Timeout from biller'


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_invalid_transaction_amount(client):
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    bill.balance = None
    with pytest.raises(ValueError):
        bill.pay(None)


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_bills')
def test_bills_list(client):
    bills = client.bills.list()
    assert bills
    assert type(bills) is list
    assert all(isinstance(bill, Bill) for bill in bills)
