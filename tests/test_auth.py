import json

from arcus.auth import base64_md5, \
    compute_md5_header, \
    calculate_checksum, \
    compute_auth_header

DICT = dict(account_id=40, account_number='501000000007')
DICT_MD5 = 'lxllA6QjrbEADpYJYMxl2w=='
SECRET_KEY = 'verify-secret'
API_KEY = 'abcdefghi123456'
CHECKSUM = 'nLet/JEZG9CRXHScwaQ/na4vsKQ='


def test_base64_md5():
    input = json.dumps(DICT)
    b64_str = base64_md5(input)
    assert type(b64_str) is str
    assert b64_str == DICT_MD5


def test_compute_md5_header():
    md5_header = compute_md5_header(DICT)
    assert type(md5_header[0]) is str
    assert md5_header[0] == 'Content-MD5'
    assert type(md5_header[1]) is str
    assert md5_header[1] == DICT_MD5


def test_calculate_checksum():
    endpoint = '/account'
    headers = [
        ('Content-MD5', ''),
        ('Date', 'Wed, 02 Nov 2016 17:26:52 GMT')
    ]
    checksum = calculate_checksum(endpoint, headers, SECRET_KEY)
    assert type(checksum) is str
    assert checksum == CHECKSUM


def test_compute_auth_header():
    endpoint = '/account'
    headers = [
        ('Content-MD5', ''),
        ('Date', 'Wed, 02 Nov 2016 17:26:52 GMT')
    ]
    auth_header = compute_auth_header(headers, endpoint, API_KEY, SECRET_KEY)
    assert type(auth_header) is tuple
    assert auth_header[0] == 'Authorization'
    assert auth_header[1] == f'APIAuth {API_KEY}:{CHECKSUM}'
