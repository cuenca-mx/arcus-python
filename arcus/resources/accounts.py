from .base import Resource


class Account(Resource):

    name: str
    balance: float
    minimum_balance: float
    currency: str
