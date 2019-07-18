import datetime
from dataclasses import dataclass
from typing import Union

from arcus.exc import InvalidOperation, UnprocessableEntity

from .base import Resource


@dataclass
class Transaction(Resource):
    _endpoint = '/transactions'

    id: int
    amount: float
    amount_currency: str
    transaction_fee: float
    hours_to_fulfill: int
    created_at: datetime.datetime
    status: str
    type: str
    fx_rate: float
    amount_usd: float
    total_usd: float
    hours_to_fulfill: int

    @classmethod
    def get(cls, transaction_id: Union[int, str]):
        transaction_dict = (
            cls._client.get(f'{cls._endpoint}?q[id_eq]={transaction_id}'))
        return Transaction(**transaction_dict['transactions'][0])

    def cancel(self) -> dict:
        try:
            return self._client.post('/transaction/cancel', dict(id=self.id))
        except UnprocessableEntity as ex:
            if ex.code in ['R26', 'R103']:
                raise InvalidOperation(ex.code, self.id)
            else:
                raise
