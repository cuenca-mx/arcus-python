import pytest

from arcus.exc import NotFound


@pytest.mark.vcr
def test_mexican_biller_list(client):
    biller_list = client.billers.list(country='MX', currency='MXN')
    assert all(
        biller.country == 'MX' and biller.currency == 'MXN'
        for biller in biller_list
    )


@pytest.mark.vcr
def test_electricity_biller_list(client):
    biller_list = client.billers.list(biller_type='Electricity')
    assert all(biller.biller_type == 'Electricity' for biller in biller_list)


@pytest.mark.vcr
def test_billers_get(client):
    biller = client.billers.get(1)
    assert biller.id == 1

    with pytest.raises(NotFound):
        client.billers.get(77777777)
