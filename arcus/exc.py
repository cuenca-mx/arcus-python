from typing import Union


class ArcusException(Exception):
    """Generic Arcus API exception"""


class InvalidAuth(ArcusException):
    def __init__(self, value: str):
        self.value = value


class InvalidAccountNumber(ArcusException):
    def __init__(self, account_number: str):
        self.message = f'{account_number} is an invalid account_number'


class InvalidBiller(ArcusException):
    def __init__(self, biller_id: Union[int, str]):
        self.message = f'{biller_id} is an invalid biller_id'


class BadRequest(ArcusException):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


class Forbidden(ArcusException):
    def __init__(self, message: str):
        self.message = message


class NotFound(ArcusException):
    def __init__(self, message: str):
        self.message = message


class UnprocessableEntity(ArcusException):
    def __init__(self, value: str, code: str, message: str, id: int):
        self.value = value
        self.code = code
        self.message = message
        self.id = id


class TooManyRequests(ArcusException):
    def __init__(self, message: str):
        self.message = message


class InternalServerError(ArcusException):
    def __init__(self, message: str):
        self.message = message


class ServiceUnavailable(ArcusException):
    def __init__(self, message: str):
        self.message = message


class UnknownStatusCode(ArcusException):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
