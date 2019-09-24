from typing import Optional, Union

from requests import HTTPError


class ArcusException(Exception):
    """Generic Arcus API exception"""


class InvalidAuth(ArcusException):
    """Invalid API authentication credentials"""


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
        return (
            self.__class__.__name__
            + '('
            + ', '.join(
                [
                    f'{attr}={repr(value)}'
                    for attr, value in self.__dict__.items()
                ]
            )
            + ')'
        )

    def __str__(self):
        return getattr(self, 'message', self.__class__.__doc__)


class InvalidAccountNumber(UnprocessableEntity):
    def __init__(self, code: str, account_number: str, biller_id: int):
        message = (
            f'{account_number} is an invalid account_number for biller '
            f'{biller_id}'
        )
        super().__init__(
            code, message, biller_id=biller_id, account_number=account_number
        )


class InvalidOperation(UnprocessableEntity):
    def __init__(self, code: str, transaction_id: Union[int, str]):
        message = f'Unable to cancel the transaction {transaction_id}'
        super().__init__(code, message, transaction_id=transaction_id)


class InvalidAmount(UnprocessableEntity):
    pass


class AlreadyPaid(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Payment already made'
        super().__init__(code, message)


class RecurrentPayments(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Recurrent payments enabled'
        super().__init__(code, message)


class DuplicatedPayment(UnprocessableEntity):
    def __init__(self, code: str, amount: float):
        message = f'Duplicated payment for {amount}'
        super().__init__(code, message, amount=amount)


class IncompleteAmount(UnprocessableEntity):
    def __init__(self, code: str, amount: float):
        message = (
            f'Incomplete payment amount of {amount}, must pay full balance'
        )
        super().__init__(code, message, amount=amount)


class Forbidden(ArcusException):
    """Method Not Allowed"""
