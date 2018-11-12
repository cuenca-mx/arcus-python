import requests
import json

from arcus import authtools
from exc import InvalidAuth

CLIENT_VERSION = '4.0.1'
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
        return self.request('get', endpoint, None, **kwargs)

    def post(self, endpoint: str, data: dict, **kwargs) -> dict:

        return self.request('post', endpoint, data, **kwargs)

    def request(self, method: str, endpoint: str, data: dict, **kwargs) -> dict:
        if data is not None:
            data = json.dumps(data)

        url = self._get_url(endpoint)
        headers = self._get_headers(endpoint=endpoint, data=data)

        response = requests.request(method, url, headers=headers, data=data)

        if response.status_code == 401:
            raise InvalidAuth('Invalid API authentication credentials')

        return response.json()

    def _get_headers(self, **kwargs):
        headers = {
            'User-Agent': CLIENT_VERSION,
            'Accept': f'application/vnd.regalii.v{self.api_version}+json',
            'Content-type': CONTENT_TYPE
        }

        self._set_md5_header(headers, kwargs['data'])
        self._set_date_header(headers)
        self._set_auth_header(headers, kwargs['endpoint'])

        return headers

    def _get_url(self, endpoint):
        return f'{self.base_url}/{endpoint}'

    def _set_md5_header(self, headers, data):
        headers['Content-MD5'] = authtools.get_md5(data)

    def _set_date_header(self, headers):
        headers['Date'] = authtools.get_timestamp()

    def _set_auth_header(self, headers, endpoint):
        content_type = CONTENT_TYPE
        content_md5 = headers['Content-MD5']
        date = headers['Date']

        data = f'{content_type},{content_md5},/{endpoint},{date}'
        checksum = authtools.get_checksum(data, self.secret_key)

        headers['Authorization'] = f'APIAuth {self.api_key}:{checksum}'
