import hmac

from hashlib import sha1, md5
from base64 import b64encode
from datetime import datetime

import pytz


def get_checksum(data, secret_key):
    """
    Computes data checksum

    The checksum is a Base64 SHA1 HMAC string encoded using your private secret key.

    :param data: Value to be computed
    :param secret_key: secret key api
    :return: Base64 SHA1 HMAC string encoded
    """
    secret_key = bytes(secret_key.encode('utf-8'))
    data = bytes(data.encode('utf-8'))

    hashed_value = hmac.new(secret_key, data, sha1)

    return b64encode(hashed_value.digest()).decode('ascii')


def get_md5(data):
    """Computes md5 Base64 string"""
    if not data:
        return ''

    digest = md5(data.encode('ascii')).digest()
    b64 = b64encode(digest).decode('ascii')

    return b64


def get_timestamp():
    """Gets current date and time"""
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(pytz.timezone('GMT'))
    return date.strftime('%a, %d %b %Y %H:%M:%S ') + 'GMT'
