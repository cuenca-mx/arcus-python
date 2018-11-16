class InvalidAuth(Exception):
    def __init__(self, value: str):
        self.value = value


class BadRequest(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


class Forbidden(Exception):
    def __init__(self, message: str):
        self.message = message


class NotFound(Exception):
    def __init__(self, message: str):
        self.message = message


class UnprocessableEntity(Exception):
    def __init__(self, value: str, code: str, message: str, id: int):
        self.value = value
        self.code = code
        self.message = message
        self.id = id


class TooManyRequests(Exception):
    def __init__(self, message: str):
        self.message = message


class InternalServerError(Exception):
    def __init__(self, message: str):
        self.message = message


class ServiceUnavailable(Exception):
    def __init__(self, message: str):
        self.message = message


class UnknownStatusCode(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
