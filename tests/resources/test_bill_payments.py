import pytest

from arcus.exc import InvalidAccountNumber, UnprocessableEntity
from arcus.resources import BillPayment


@pytest.mark.vcr
def test_bill_payment(client):
    biller_id = 13599
    account_number = '5599999999'
    amount = 100.0
    bill_payment = client.bill_payments.create(
        biller_id, account_number, amount
    )
    assert bill_payment.biller_id == biller_id
    assert bill_payment.account_number == account_number
    assert bill_payment.bill_amount == amount
    assert bill_payment.ending_balance < bill_payment.starting_balance
    assert bill_payment.chain_earned + bill_payment.chain_paid == amount


@pytest.mark.vcr
def test_bill_payment_with_int(client):
    biller_id = 13599
    account_number = '5599999999'
    amount = 100
    with pytest.raises(TypeError):
        client.bill_payments.create(biller_id, account_number, amount)


@pytest.mark.vcr
def test_bill_payment_invalid_phone_number(client):
    biller_id = 13599
    account_number = '559999'
    amount = 100.0
    with pytest.raises(InvalidAccountNumber) as excinfo:
        client.bill_payments.create(biller_id, account_number, amount)
    exc = excinfo.value
    assert exc.account_number == account_number
    assert exc.biller_id == biller_id


@pytest.mark.vcr
def test_bill_payment_type_error(client):
    biller_id = 13599
    account_number = '559999'
    amount = 100.0
    with pytest.raises(UnprocessableEntity) as excinfo:
        client.bill_payments.create(biller_id, account_number, amount)
    exc = excinfo.value
    assert exc.account_number == account_number
    assert exc.biller_id == biller_id


def test_bill_payment_list(client):
    with pytest.raises(NotImplementedError):
        client.bill_payments.list()


@pytest.mark.vcr
def test_pay_invoice_with_name_on_account(client):
    biller_id = 1781
    account_number = '5599999999'
    amount = 578.0
    invoice_owner = 'Edward S. Burton'
    bill_payment = client.bill_payments.create(
        biller_id, account_number, amount, name_on_account=invoice_owner
    )
    assert bill_payment.biller_id == biller_id
    assert bill_payment.account_number == account_number
    assert bill_payment.bill_amount == amount
    assert bill_payment.ending_balance < bill_payment.starting_balance


def test_unimplemented():
    with pytest.raises(NotImplementedError):
        BillPayment.list()
    with pytest.raises(NotImplementedError):
        BillPayment.get(1)
