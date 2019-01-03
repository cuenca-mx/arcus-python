from typing import Optional, Union

from arcus.exc import (
    ArcusException, InvalidAccountNumber, InvalidBiller, NotFound,
    UnprocessableEntity)

from .base import Resource
from .transactions import Transaction


class Bill(Resource):
    _endpoint = '/bills'

    @staticmethod
    def _handle_exception(
            ex: ArcusException,
            biller_id: Union[int, str],
            account_number: str
    ):
        ex_type = type(ex)
        if ex_type is NotFound:
            raise InvalidBiller(biller_id)
        elif ex_type is UnprocessableEntity and ex.code == 'R2':
            raise InvalidAccountNumber(account_number)
        else:
            raise ex

    @classmethod
    def create(cls, biller_id: Union[int, str], account_number: str):
        data = dict(biller_id=biller_id, account_number=account_number)
        try:
            bill_dict = cls._client.post(cls._endpoint, data)
        except ArcusException as ex:
            cls._handle_exception(ex, biller_id, account_number)
        else:
            return cls(**bill_dict)

    def pay(self, amount: Optional[float] = None) -> Transaction:
        amount = amount or self.balance
        data = dict(amount=amount, currency=self.balance_currency)
        transaction_dict = self._client.post(
            f'{self._endpoint}/{self.id}/pay', data)
        return Transaction(**transaction_dict)
