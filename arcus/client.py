import requests
import json

from arcus import authtools
from arcus.exc import InvalidAuth


API_VERSION = '3.1'
PRODUCTION_API_URL = 'https://api.regalii.com'
SANDBOX_API_URL = 'https://api.casiregalii.com'
CONTENT_TYPE = 'application/json'


class Client:

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            sandbox: bool = False,
            api_version: str = API_VERSION
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        if sandbox:
            self.base_url = SANDBOX_API_URL
        else:
            self.base_url = PRODUCTION_API_URL
        self.api_version = api_version

    def get(self, endpoint: str, **kwargs) -> dict:
        return self.request('get', endpoint, {}, **kwargs)

    def post(self, endpoint: str, data: dict, **kwargs) -> dict:
        return self.request('post', endpoint, data, **kwargs)

    def request(self,
                method: str,
                endpoint: str,
                data: dict,
                **kwargs) -> dict:
        url = self.base_url + endpoint
        headers = self._build_headers(endpoint, data)

        response = requests.request(
            method, url, headers=headers, json=data, **kwargs)

        if response.status_code == 401:
            raise InvalidAuth('Invalid API authentication credentials')

        return response.json()

    def _build_headers(self, endpoint, data):
        headers = [
            ('Accept', f'application/vnd.regalii.v{self.api_version}+json')
        ]
        headers.append(self._compute_md5_header(data))
        headers.append(self._compute_date_header())
        headers.append(self._compute_auth_header(headers, endpoint))
        return dict(headers)

    @staticmethod
    def _compute_md5_header(data):
        data = json.dumps(data)
        return 'Content-MD5', authtools.get_md5(data)

    @staticmethod
    def _compute_date_header():
        return 'Date', authtools.get_timestamp()

    def _compute_auth_header(self, headers, endpoint):
        content_type = CONTENT_TYPE
        headers = dict(headers)
        content_md5 = headers['Content-MD5']
        date = headers['Date']

        data = f'{content_type},{content_md5},{endpoint},{date}'
        checksum = authtools.get_checksum(data, self.secret_key)

        return 'Authorization', f'APIAuth {self.api_key}:{checksum}'
