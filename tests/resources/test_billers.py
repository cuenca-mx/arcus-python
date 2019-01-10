import vcr

from ..fixtures import client


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_billers')
def test_mexican_biller_list(client):
    biller_list = client.biller.list(country='MX', currency='MXN')

    assert all(biller.country == 'MX' and
               biller.currency == 'MXN' for biller in biller_list)


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_billers')
def test_electricity_biller_list(client):
    biller_list = client.biller.list(biller_type='Electricity')

    assert all(biller.biller_type == 'Electricity' for biller in biller_list)
