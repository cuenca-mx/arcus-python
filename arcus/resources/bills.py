from typing import Optional, Union

from arcus.exc import (
    InvalidAccountNumber, InvalidBiller, NotFound, UnprocessableEntity)

from .base import Resource
from .transactions import Transaction


class Bill(Resource):
    _endpoint = '/bills'

    def __init__(
            self,
            id: int,
            biller_id: int,
            account_number: str,
            balance: float,
            balance_currency: str,
            **kwargs
    ):
        self.id = id
        self.biller_id = biller_id
        self.account_number = account_number
        self.balance = balance
        self.balance_currency = balance_currency
        super().__init__(**kwargs)

    @classmethod
    def create(cls, biller_id: Union[int, str], account_number: str):
        data = dict(biller_id=biller_id, account_number=account_number)
        try:
            bill_dict = cls._client.post(cls._endpoint, data)
        except NotFound:
            raise InvalidBiller(biller_id)
        except UnprocessableEntity as ex:
            if ex.code == 'R2':
                raise InvalidAccountNumber(account_number)
            else:
                raise
        else:
            return cls(**bill_dict)

    def pay(self, amount: Optional[float] = None) -> Transaction:
        amount = amount or self.balance
        if not amount:
            raise ValueError('amount is not specified')
        data = dict(amount=amount, currency=self.balance_currency)
        transaction_dict = self._client.post(
            f'{self._endpoint}/{self.id}/pay', data)
        return Transaction(**transaction_dict)
