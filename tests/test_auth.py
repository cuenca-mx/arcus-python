import json

from arcus.auth import (
    base64_md5,
    calculate_checksum,
    compute_auth_header,
    compute_md5_header,
)

ACCOUNT_INFO = dict(account_id=40, account_number='501000000007')
ACCOUNT_INFO_MD5 = 'lxllA6QjrbEADpYJYMxl2w=='
SECRET_KEY = 'verify-secret'
API_KEY = 'abcdefghi123456'
CHECKSUM = 'nLet/JEZG9CRXHScwaQ/na4vsKQ='


def test_base64_md5():
    json_dump = json.dumps(ACCOUNT_INFO)
    b64_str = base64_md5(json_dump)
    assert b64_str == ACCOUNT_INFO_MD5


def test_compute_md5_header():
    header_key, header_value = compute_md5_header(ACCOUNT_INFO)
    assert header_key == 'Content-MD5'
    assert header_value == ACCOUNT_INFO_MD5


def test_calculate_checksum():
    endpoint = '/account'
    headers = [('Content-MD5', ''), ('Date', 'Wed, 02 Nov 2016 17:26:52 GMT')]
    checksum = calculate_checksum(endpoint, headers, SECRET_KEY)
    assert type(checksum) is str
    assert checksum == CHECKSUM


def test_compute_auth_header():
    endpoint = '/account'
    headers = [('Content-MD5', ''), ('Date', 'Wed, 02 Nov 2016 17:26:52 GMT')]
    header_key, header_value = compute_auth_header(
        headers, endpoint, API_KEY, SECRET_KEY
    )
    assert header_key == 'Authorization'
    assert header_value == f'APIAuth {API_KEY}:{CHECKSUM}'
