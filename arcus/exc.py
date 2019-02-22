from typing import Optional, Union

from requests import HTTPError


class ArcusException(Exception):
    """Generic Arcus API exception"""


class InvalidAuth(ArcusException):
    """Invalid API authentication credentials"""


class InvalidAccountNumber(ArcusException):
    def __init__(self, account_number: str):
        self.message = f'{account_number} is an invalid account_number'


class InvalidBiller(ArcusException):
    def __init__(self, biller_id: Union[int, str]):
        self.message = f'{biller_id} is an invalid biller_id'


class NotFound(ArcusException, HTTPError):
    pass


class UnprocessableEntity(ArcusException):
    def __init__(self, code: str, message: Optional[str] = None, **kwargs):
        self.code = code
        if message:
            self.message = message
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __repr__(self):
        return self.__class__.__name__ + ', '.join(
            [f'{attr}={repr(value)}'
             for attr, value in self.__dict__.items()]) + ')'

    def __str__(self):
        return getattr(self, 'message', self.__class__.__doc__)


class InvalidOperation(UnprocessableEntity):
    def __init__(self, code: str, transaction_id: Union[int, str]):
        self.message = f'Unable to cancel the transaction {transaction_id}'
        super().__init__(code, self.message,
                         transaction_id=transaction_id)
