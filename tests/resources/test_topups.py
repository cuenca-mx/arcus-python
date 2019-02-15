import pytest

from arcus.exc import UnprocessableEntity


@pytest.mark.vcr
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


@pytest.mark.vcr
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


@pytest.mark.vcr
def test_pay_invoice_with_name_on_account(client):
    biller_id = 1781
    account_number = '5599999999'
    amount = 578.0
    invoice_owner = 'Edward S. Burton'
    topup = client.topups.create(biller_id, account_number, amount,
                                 name_on_account=invoice_owner)
    assert topup.biller_id == biller_id
    assert topup.account_number == account_number
    assert topup.bill_amount == amount
    assert topup.ending_balance < topup.starting_balance
