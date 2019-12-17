import os
from typing import Dict, Optional, Union

import requests

from .api_keys import ApiKey
from .auth import compute_auth_header, compute_date_header, compute_md5_header
from .exc import Forbidden, InvalidAuth, NotFound, UnprocessableEntity
from .resources import (
    Account,
    Bill,
    Biller,
    BillPayment,
    Resource,
    Transaction,
)

API_VERSION = '3.1'
PRODUCTION_API_URL = 'https://api.regalii.com'
SANDBOX_API_URL = 'https://api.casiregalii.com'


class Client:

    bills = Bill
    billers = Biller
    bill_payments = BillPayment
    transactions = Transaction

    def __init__(
        self,
        primary_user: Optional[str] = None,
        primary_secret: Optional[str] = None,
        topup_user: Optional[str] = None,
        topup_secret: Optional[str] = None,
        sandbox: bool = False,
        # refers to: https://github.com/cuenca-mx/arcus-read-only
        proxy: Optional[str] = None,
    ):
        self.headers: Dict[str, str] = dict()
        self.session = requests.Session()
        self.sandbox = sandbox
        self.proxy = proxy
        self.api_key = ApiKey(
            primary_user or os.environ['ARCUS_API_KEY'],
            primary_secret or os.environ['ARCUS_SECRET_KEY'],
        )

        self.topup_key: Optional[ApiKey]
        try:
            self.topup_key = ApiKey(
                topup_user or os.environ.get('TOPUP_API_KEY') or '',
                topup_secret or os.environ.get('TOPUP_SECRET_KEY') or '',
            )
        except ValueError:
            self.topup_key = None

        if not proxy:
            if sandbox:
                self.base_url = SANDBOX_API_URL
            else:
                self.base_url = PRODUCTION_API_URL
        else:
            self.base_url = proxy
            self.headers['X-ARCUS-SANDBOX'] = str(sandbox).lower()
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
        api_key: Union[str, ApiKey]
        if not self.proxy:
            if topup and self.topup_key:
                api_key = self.topup_key
            else:
                api_key = self.api_key
            headers = self._build_headers(api_key, endpoint, api_version, data)
        else:
            if topup and self.topup_key:
                api_key = self.topup_key.user
            else:
                api_key = self.api_key.user
            headers = {'X-ARCUS-API-KEY': api_key}
            # GET request with Body is not allowed on CloudFront
            data = dict()
        response = self.session.request(
            method,
            url,
            headers={**self.headers, **headers},
            json=data if data else None,
            **kwargs,
        )
        self._check_response(response)
        return response.json()

    @property
    def accounts(self) -> Dict[str, Account]:
        if self.proxy:
            accounts_dict = self.get('/account')
            accounts_ = {
                key: Account(**val) for key, val in accounts_dict.items()
            }
        else:
            accounts_ = dict(primary=Account(**self.get('/account')))
            if self.topup_key:
                accounts_['topup'] = Account(
                    **self.get('/account', topup=True)
                )
        return accounts_

    @staticmethod
    def _build_headers(
        api_key: ApiKey, endpoint: str, api_version: str, data: dict
    ) -> dict:
        headers = list()
        headers.append(
            ('Accept', f'application/vnd.regalii.v{api_version}+json')
        )
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
            response.raise_for_status()  # pragma: no cover
