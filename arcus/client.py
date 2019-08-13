import os
from typing import List, Optional

import requests

from .api_keys import ApiKey
from .auth import compute_auth_header, compute_date_header, compute_md5_header
from .exc import Forbidden, InvalidAuth, NotFound, UnprocessableEntity
from .resources import Account, Bill, Biller, Resource, Topup, Transaction

API_VERSION = '3.1'
PRODUCTION_API_URL = 'https://api.regalii.com'
SANDBOX_API_URL = 'https://api.casiregalii.com'


class Client:

    bills = Bill
    billers = Biller
    topups = Topup
    transactions = Transaction

    def __init__(
        self,
        primary_user: Optional[str] = None,
        primary_secret: Optional[str] = None,
        topup_user: Optional[str] = None,
        topup_secret: Optional[str] = None,
        sandbox: bool = False,
        proxy: Optional[str] = None,  # Used in the case of a read-only proxy
    ):
        self.headers = {}
        self.session = requests.Session()
        self.sandbox = sandbox
        self.proxy = proxy
        if not proxy:
            self.api_key = ApiKey(
                primary_user or os.environ['ARCUS_API_KEY'],
                primary_secret or os.environ['ARCUS_SECRET_KEY'],
            )
            try:
                self.topup_key = ApiKey(
                    topup_user or os.environ.get('TOPUP_API_KEY'),
                    topup_secret or os.environ.get('TOPUP_SECRET_KEY'),
                )
            except ValueError:
                self.topup_key = None
            if sandbox:
                self.base_url = SANDBOX_API_URL
            else:
                self.base_url = PRODUCTION_API_URL
        else:
            self.api_key = None
            self.topup_key = None
            self.base_url = proxy
            if sandbox:
                self.headers['X-ARCUS-SANDBOX'] = 'true'
            else:
                self.headers['X-ARCUS-SANDBOX'] = 'false'

        Resource._client = self

    def get(self, endpoint: str, **kwargs) -> dict:
        return self.request('get', endpoint, {}, **kwargs)

    def post(self, endpoint: str, data: dict, **kwargs) -> dict:
        return self.request('post', endpoint, data, **kwargs)

    def request(
        self,
        method: str,
        endpoint: str,
        data: dict,
        api_version: str = API_VERSION,
        topup: bool = False,
        **kwargs,
    ) -> dict:
        url = self.base_url + endpoint
        if not self.proxy:
            if topup and self.topup_key:
                api_key = self.topup_key
            else:
                api_key = self.api_key
            headers = self._build_headers(api_key, endpoint, api_version, data)
            response = self.session.request(
                method, url, headers=headers, json=data, **kwargs
            )
        else:
            headers = {}  # The proxy is going to sign the request
            headers = {**headers, **self.headers}
            response = self.session.request(
                method, url, headers=headers, **kwargs
            )
        self._check_response(response)
        return response.json()

    @property
    def accounts(self) -> List[Account]:
        accounts_ = [Account(**self.get('/account'))]
        if self.topup_key:
            accounts_.append(Account(**self.get('/account', topup=True)))
        return accounts_

    @staticmethod
    def _build_headers(
        api_key: ApiKey, endpoint: str, api_version: str, data: dict
    ) -> dict:
        headers = [('Accept', f'application/vnd.regalii.v{api_version}+json')]
        headers.append(compute_md5_header(data))
        headers.append(compute_date_header())
        headers.append(
            compute_auth_header(
                headers, endpoint, api_key.user, api_key.secret
            )
        )
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
        elif response.status_code in [400, 422]:
            raise UnprocessableEntity(**data)
        elif response.status_code == 403:
            raise Forbidden
        else:
            response.raise_for_status()
