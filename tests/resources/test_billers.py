import vcr

from ..fixtures import client


@vcr.use_cassette(cassette_library_dir='tests/cassettes/test_billers')
def test_biller_list(client):
    biller_list = client.biller.list('MX', 'MXN')

    N = len(biller_list)
    for x in range(0, N):
        assert biller_list[x]['country'] == 'MX' and \
               biller_list[x]['currency'] == 'MXN'
