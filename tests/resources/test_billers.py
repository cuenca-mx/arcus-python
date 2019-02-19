import pytest


@pytest.mark.vcr
def test_mexican_biller_list(client):
    biller_list = client.billers.list(country='MX', currency='MXN')
    assert all(biller.country == 'MX' and
               biller.currency == 'MXN' for biller in biller_list)


@pytest.mark.vcr
def test_electricity_biller_list(client):
    biller_list = client.billers.list(biller_type='Electricity')
    assert all(biller.biller_type == 'Electricity' for biller in biller_list)


def test_billers_get(client):
    with pytest.raises(NotImplementedError):
        client.billers.get(1)
