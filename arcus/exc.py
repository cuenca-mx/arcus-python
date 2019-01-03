from typing import Union

from requests import HTTPError


class ArcusException(Exception):
    message = """Generic Arcus API exception"""


class InvalidAuth(ArcusException):
    message = """Invalid API authentication credentials"""


class InvalidAccountNumber(ArcusException):
    def __init__(self, account_number: str):
        self.message = f'{account_number} is an invalid account_number'


class InvalidBiller(ArcusException):
    def __init__(self, biller_id: Union[int, str]):
        self.message = f'{biller_id} is an invalid biller_id'


class NotFound(ArcusException, HTTPError):
    pass


class UnprocessableEntity(ArcusException):
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __repr__(self):
        attrs = {}
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                value = f"'{value}'"
            attrs[attr] = value
        return self.__class__.__name__ + ', '.join(
            [f'{attr}={value}' for attr, value in attrs.items()]) + ')'
