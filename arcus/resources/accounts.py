from dataclasses import dataclass

from .base import Resource


@dataclass
class Account(Resource):

    name: str
    balance: float
    minimum_balance: float
    currency: str
