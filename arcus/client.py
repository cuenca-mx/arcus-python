import os
from typing import Optional

import requests

from .auth import compute_auth_header, compute_date_header, compute_md5_header
from .resources import Account, Bill, Resource, Topup, Transaction
from .exc import InvalidAuth, NotFound, UnprocessableEntity


API_VERSION = '3.1'
PRODUCTION_API_URL = 'https://api.regalii.com'
SANDBOX_API_URL = 'https://api.casiregalii.com'


class Client:

    bills = Bill
    transactions = Transaction
    topups = Topup

    def __init__(
            self,
            api_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            sandbox: bool = False
    ):
        self.api_key = api_key or os.environ['ARCUS_API_KEY']
        self.secret_key = secret_key or os.environ['ARCUS_SECRET_KEY']
        if sandbox:
            self.base_url = SANDBOX_API_URL
        else:
            self.base_url = PRODUCTION_API_URL
        Resource._client = self

    def get(self, endpoint: str, **kwargs) -> dict:
        return self.request('get', endpoint, {}, **kwargs)

    def post(self, endpoint: str, data: dict, **kwargs) -> dict:
        return self.request('post', endpoint, data, **kwargs)

    def request(self,
                method: str,
                endpoint: str,
                data: dict,
                api_version: str = API_VERSION,
                **kwargs) -> dict:
        url = self.base_url + endpoint
        headers = self._build_headers(endpoint, api_version, data)
        response = requests.request(
            method, url, headers=headers, json=data, **kwargs)
        self._check_response(response)
        return response.json()

    @property
    def account(self):
        return Account(**self.get('/account'))

    def _build_headers(self,
                       endpoint: str,
                       api_version: str,
                       data: dict) -> dict:
        headers = [('Accept',
                    f'application/vnd.regalii.v{api_version}+json')]
        headers.append(compute_md5_header(data))
        headers.append(compute_date_header())
        headers.append(compute_auth_header(
            headers, endpoint, self.api_key, self.secret_key))
        return dict(headers)

    @staticmethod
    def _check_response(response):
        if response.ok:
            return
        data = response.json()
        if response.status_code == 401:
            raise InvalidAuth
        elif response.status_code == 404:
            raise NotFound(data['message'])
        elif response.status_code == 422:
            raise UnprocessableEntity(**data)
        else:
            response.raise_for_status()
