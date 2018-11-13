import hmac
import json
from base64 import b64encode
from datetime import datetime
from hashlib import sha1, md5

import pytz


CONTENT_TYPE = 'application/json'


def compute_md5_header(data: dict) -> tuple:
    data = json.dumps(data)
    return 'Content-MD5', base64_md5(data)


def compute_date_header() -> tuple:
    return 'Date', compute_timestamp()


def compute_auth_header(
        headers: list,
        endpoint: str,
        api_key: str,
        secret_key: str) -> tuple:
    verify_secret = calculate_checksum(endpoint, headers, secret_key)
    return 'Authorization', f'APIAuth {api_key}:{verify_secret}'


def calculate_checksum(endpoint: str, headers: list,
                       secret_key: str) -> str:
    """
    Calculate checksum based on https://www.arcusfi.com/api/v3/#authentication
    """
    headers = dict(headers)
    content_md5 = headers['Content-MD5']
    date = headers['Date']
    verify_this = f'{CONTENT_TYPE},{content_md5},{endpoint},{date}'
    verify_secret = hmac.new(
        secret_key.encode('utf-8'), verify_this.encode('utf-8'), sha1)
    return b64encode(verify_secret.digest()).decode('ascii')


def base64_md5(data: str) -> str:
    """base64 encoded md5 hash"""
    digest = md5(data.encode('ascii')).digest()
    b64 = b64encode(digest).decode('ascii')
    return b64


def compute_timestamp() -> str:
    """
    Gets current date and time
    Based on https://github.com/regalii/regaliator_python/blob/master/regalii/
        clients/__init__.py#L67
    """
    now = datetime.now(tz=pytz.utc).astimezone(pytz.timezone('GMT'))
    return now.strftime('%a, %d %b %Y %H:%M:%S ') + 'GMT'
