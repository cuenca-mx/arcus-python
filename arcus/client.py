import requests

from .auth import compute_auth_header, compute_date_header, compute_md5_header
from .resources import Account, Bill, Resource, Transaction
from .exc import (
    BadRequest, InvalidAuth, Forbidden, NotFound, TooManyRequests,
    InternalServerError, ServiceUnavailable, UnprocessableEntity)


API_VERSION = '3.1'
PRODUCTION_API_URL = 'https://api.regalii.com'
SANDBOX_API_URL = 'https://api.casiregalii.com'


class Client:

    bills = Bill

    transactions = Transaction

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
        Resource._client = self

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
        self._check_response(response)
        return response.json()

    @property
    def account(self):
        return Account(**self.get('/account'))

    def _build_headers(self, endpoint: str, data: dict) -> dict:
        headers = [('Accept',
                    f'application/vnd.regalii.v{self.api_version}+json')]
        headers.append(compute_md5_header(data))
        headers.append(compute_date_header())
        headers.append(compute_auth_header(
            headers, endpoint, self.api_key, self.secret_key))
        return dict(headers)

    @staticmethod
    def _check_response(response):
        if response.status_code in (200, 201):
            return
        try:
            data = response.json()
        except Exception:
            data = dict()
        if response.status_code == 400:
            raise BadRequest('Invalid request message')
        elif response.status_code == 401:
            raise InvalidAuth('Invalid API authentication credentials')
        elif response.status_code == 403:
            raise Forbidden('You are not authorized to access'
                            ' the resource requested')
        elif response.status_code == 404:
            raise NotFound('Resource not found')
        elif response.status_code == 422:
            raise UnprocessableEntity('Unprocessable Entity',
                                      data['code'],
                                      data['message'],
                                      data['id'] if 'id' in data else None)
        elif response.status_code == 429:
            raise TooManyRequests('You’re sending too many requests!')
        elif response.status_code == 500:
            raise InternalServerError('We had a problem with our server. '
                                      'Try again later.')
        elif response.status_code == 503:
            raise ServiceUnavailable('Service Unavailable – '
                                     'Please try again later')
