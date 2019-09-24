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
    def __init__(self, code: str, amount: float):
        message = f'Invalid amount: {amount}'
        super().__init__(code, message)


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


class UnexpectedError(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Unexpected error. Failed to make the consult'
        super().__init__(code, message)


class InvalidOrMissingParameters(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Invalid or missing parameters'
        super().__init__(code, message)


class InvalidBalance(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Account Balance is 0 or not enough'
        super().__init__(code, message)


class FailedConsult(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Failed to make the consult, please try again later'
        super().__init__(code, message)


class LimitExceeded(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Limit of transactions exceeded'
        super().__init__(code, message)


class BillerMaintenance(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Biller maintenance in progress, please try again later'
        super().__init__(code, message)


class ReversalNotSupported(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Reversal not supported'
        super().__init__(code, message)


class BillerConnection(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Timeout from biller'
        super().__init__(code, message)


class CancellationError(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Error with performing the cancellation'
        super().__init__(code, message)


class OverdueBill(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Overdue Bill'
        super().__init__(code, message)


class InvalidPhone(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Invalid Phone Number'
        super().__init__(code, message)


class FraudSuspected(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Fraud suspected'
        super().__init__(code, message)


class InvalidCurrency(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Invalid Currency'
        super().__init__(code, message)


class InvalidCompany(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Invalid company'
        super().__init__(code, message)


class InvalidBarCode(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Invalid Barcode Format.'
        super().__init__(code, message)


class InvalidCustomerStatus(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Invalid Customer Status.'
        super().__init__(code, message)


class DailyPaymentsLimit(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'The maximum number of payments on this day was reached'
        super().__init__(code, message)


class BalanceNotFound(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Can\'t get balance.'
        super().__init__(code, message)


class InvalidSubscription(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Invalid Subscription ID. Verify the ID or create a new'
        super().__init__(code, message)


class InvalidPOS(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'POS number is invalid'
        super().__init__(code, message)


class AccessDenied(UnprocessableEntity):
    def __init__(self, code: str):
        message = f'Processor Access Denied'
        super().__init__(code, message)


def raiseCustomArcusException(
        ex: UnprocessableEntity,
        account_number: str,
        biller_id: int,
        amount: Optional[float] = 0):
    if ex.code in {'R1', 'R2', 'R4', 'R5', 'R10', 'R28', 'R29'}:
        raise InvalidAccountNumber(
            ex.code, account_number, biller_id)
    elif ex.code in {'R3', 'R11', 'R41'}:
        raise IncompleteAmount(ex.code, amount=amount)
    elif ex.code in {'R6', 'R19', 'R20', 'R21'}:
        raise InvalidBiller(biller_id)
    elif ex.code in {'R7', 'R37'}:
        raise RecurrentPayments(ex.code)
    elif ex.code in {'R8', 'R12'}:
        raise AlreadyPaid(ex.code)
    elif ex.code in {'R9', 'R99', 'R299'}:
        raise UnexpectedError(ex.code)
    elif ex.code in {'R13'}:
        raise InvalidOrMissingParameters(ex.code)
    elif ex.code in {'R14', 'R17', 'R32', 'R102', 'R114'}:
        raise InvalidAmount(ex.code, amount)
    elif ex.code in {'R15', 'R42', 'R100'}:
        raise InvalidBalance(ex.code)
    elif ex.code in {'R16', 'R35'}:
        raise FailedConsult(ex.code)
    elif ex.code in {'R18'}:
        raise LimitExceeded(ex.code)
    elif ex.code in {'R22'}:
        raise BillerMaintenance(ex.code)
    elif ex.code in {'R23', 'R26',  'R103', 'R105'}:
        raise ReversalNotSupported(ex.code)
    elif ex.code in {'R24', 'R47', 'R48'}:
        raise BillerConnection(ex.code)
    elif ex.code in {'R25'}:
        raise CancellationError(ex.code)
    elif ex.code in {'R27'}:
        raise OverdueBill(ex.code)
    elif ex.code in {'R30', 'R117'}:
        raise InvalidCompany(ex.code)
    elif ex.code in {'R31'}:
        raise InvalidPhone(ex.code)
    elif ex.code in {'R33'}:
        raise FraudSuspected(ex.code)
    elif ex.code in {'R34'}:
        raise InvalidCurrency(ex.code)
    elif ex.code in {'R36'}:
        raise DuplicatedPayment(ex.code, amount=amount)
    elif ex.code in {'R43'}:
        raise InvalidBarCode(ex.code)
    elif ex.code in {'R44'}:
        raise InvalidCustomerStatus(ex.code)
    elif ex.code in {'R45'}:
        raise DailyPaymentsLimit(ex.code)
    elif ex.code in {'R46', 'R101', 'R121', 'R122', 'R202'}:
        raise BalanceNotFound(ex.code)
    elif ex.code in {'R104'}:
        raise InvalidSubscription(ex.code)
    elif ex.code in {'R117'}:
        raise InvalidPOS(ex.code)
    elif ex.code in {'R201'}:
        raise AccessDenied(ex.code)
    else:
        raise
