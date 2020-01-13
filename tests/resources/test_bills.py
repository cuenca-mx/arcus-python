import pytest

from arcus import exc
from arcus.resources import Bill


@pytest.mark.vcr
def test_create_bill(client):
    bill = client.bills.create(40, '501000000007')
    assert type(bill) is Bill
    assert bill.biller_id == 40
    assert bill.account_number == '501000000007'
    assert type(bill.balance) is float


@pytest.mark.vcr
def test_invalid_biller_id(client):
    invalid_biller_id = 99999999
    with pytest.raises(exc.InvalidBiller):
        client.bills.create(invalid_biller_id, '1234')


@pytest.mark.vcr
def test_invalid_account_number(client):
    biller_id = 40
    invalid_account_number = '501000000004'
    with pytest.raises(exc.InvalidAccountNumber) as excinfo:
        client.bills.create(biller_id, invalid_account_number)
    assert excinfo.value.account_number == invalid_account_number
    assert excinfo.value.biller_id == biller_id


@pytest.mark.vcr
def test_successful_payment(client):
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    transaction = bill.pay()
    assert transaction.id
    assert transaction.status == 'fulfilled'


@pytest.mark.vcr
def test_amount_too_low(client):
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    with pytest.raises(exc.InvalidAmount):
        bill.pay(0.01)


@pytest.mark.vcr
def test_pay_with_int_amount(client):
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    with pytest.raises(TypeError):
        bill.pay(100)


@pytest.mark.vcr
def test_unexpected_error(client):
    with pytest.raises(exc.UnexpectedError) as excinfo:
        client.bills.create(6900, '1111362009')
    e = excinfo.value
    assert e.code == 'R9'
    str(e)


@pytest.mark.vcr
def test_cancel_bill_success(client):
    bill = client.bills.create(35, '123456851236')
    transaction = bill.pay(bill.balance)
    cancellation = transaction.cancel()
    assert cancellation['code'] == 'R0'
    assert cancellation['message'] == 'Transaction successful'

    updated_transaction = client.transactions.get(transaction.id)
    assert updated_transaction.id == transaction.id
    assert updated_transaction.status == 'refunded'
    assert transaction.status == updated_transaction.status


@pytest.mark.vcr
def test_cancel_bill_fail(client):
    first_bill = client.bills.create(35, '123456851236')
    first_transaction = first_bill.pay(first_bill.balance)
    first_transaction.cancel()
    with pytest.raises(exc.InvalidOperation) as excinfo:
        first_transaction.cancel()
    assert excinfo.value.code == 'R103'
    assert excinfo.value.message == (
        f'Unable to cancel the transaction {first_transaction.id}'
    )

    second_bill = client.bills.create(37, '7259047384')
    second_transaction = second_bill.pay(second_bill.balance)
    with pytest.raises(exc.InvalidOperation) as excinfo:
        second_transaction.cancel()
    assert excinfo.value.code == 'R26'
    assert excinfo.value.message == (
        f'Unable to cancel the transaction {second_transaction.id}'
    )


@pytest.mark.vcr
def test_consult_error(client):
    with pytest.raises(exc.UnprocessableEntity) as excinfo:
        client.bills.create(2901, '1111322016')
    e = excinfo.value
    assert repr(e)
    assert e.code == 'R16'
    assert e.message == 'Failed to make the consult, please try again later'


@pytest.mark.vcr
def test_biller_maintenance(client):
    with pytest.raises(exc.BillerMaintenance) as excinfo:
        client.bills.create(1821, '1111992022')
    e = excinfo.value
    assert e.code == 'R22'
    assert e.message == (
        'Biller maintenance in progress, please try again later'
    )


@pytest.mark.vcr
def test_timeout_on_payment(client):
    bill = client.bills.create(37, '2424240024')
    with pytest.raises(exc.BillerConnection) as excinfo:
        bill.pay()
    e = excinfo.value
    assert e.code == 'R24'
    assert e.message == 'Timeout from biller'


@pytest.mark.vcr
def test_invalid_transaction_amount(client):
    bill = client.bills.create(40, '501000000007')
    assert bill == client.bills.get(bill.id)
    bill.balance = None
    with pytest.raises(ValueError):
        bill.pay(None)


@pytest.mark.vcr
def test_bills_list(client):
    bills = client.bills.list()
    assert bills
    assert type(bills) is list
    assert all(isinstance(bill, Bill) for bill in bills)


@pytest.mark.vcr
def test_recurrent_payments(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.RecurrentPayments) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.message == 'Recurrent payments enabled'


@pytest.mark.vcr
def test_already_paid(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.AlreadyPaid) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.message == 'Payment already made'


@pytest.mark.vcr
def test_duplicate_payment(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.DuplicatedPayment) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.message == 'Duplicated payment for 549.0'


@pytest.mark.vcr
def test_incomplete_amount(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.IncompleteAmount) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert (
        ex.message
        == 'Incomplete payment amount of 549.0, must pay full balance'
    )


@pytest.mark.vcr
def test_missing_parameters(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.InvalidOrMissingParameters) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R13'
    assert ex.message == 'Invalid or missing parameters'


@pytest.mark.vcr
def test_limit_payments(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.DailyPaymentsLimit) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R45'
    assert (
        ex.message == 'The maximum number of payments on this day was reached'
    )


@pytest.mark.vcr
def test_failed_consult(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.FailedConsult) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R16'
    assert ex.message == 'Failed to make the consult, please try again later'


@pytest.mark.vcr
def test_invalid_balance(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.InvalidBalance) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R15'
    assert ex.message == 'Account Balance is 0 or not enough'


@pytest.mark.vcr
def test_invalid_currency(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.InvalidCurrency) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R34'
    assert ex.message == 'Invalid Currency'


@pytest.mark.vcr
def test_daily_limit(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.UnprocessableEntity) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R45'
    assert (
        ex.message == 'The maximum number of payments on this day was reached'
    )


@pytest.mark.vcr
def test_overdue_bill(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.OverdueBill) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R27'
    assert ex.message == 'Overdue Bill'


@pytest.mark.vcr
def test_fraud_suspected(client):
    bill = client.bills.create(40, '501000000007')
    with pytest.raises(exc.UnprocessableEntity) as excinfo:
        bill.pay()
    ex = excinfo.value
    assert ex.code == 'R33'
    assert ex.message == 'Fraud suspected'
