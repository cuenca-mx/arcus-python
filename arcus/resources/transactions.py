import datetime
from dataclasses import dataclass, field
from typing import ClassVar, Union

from arcus.exc import InvalidOperation, UnprocessableEntity

from .base import Resource


@dataclass
class Transaction(Resource):
    _endpoint: ClassVar[str] = '/transactions'

    id: int
    amount: float
    amount_currency: str
    transaction_fee: float
    hours_to_fulfill: int
    created_at: datetime.datetime
    status: str
    type: str = field(repr=False)
    fx_rate: float = field(repr=False)
    amount_usd: float = field(repr=False)
    total_usd: float = field(repr=False)

    @classmethod
    def get(cls, transaction_id: Union[int, str]):
        transaction_dict = cls._client.get(
            f'{cls._endpoint}?q[id_eq]={transaction_id}'
        )
        return Transaction(**transaction_dict['transactions'][0])

    def refresh(self):
        updated = self.get(self.id)
        for attr, value in updated.__dict__.items():
            setattr(self, attr, value)

    def cancel(self) -> dict:
        try:
            resp = self._client.post('/transaction/cancel', dict(id=self.id))
        except UnprocessableEntity as ex:
            if ex.code in ['R26', 'R103']:
                raise InvalidOperation(ex.code, self.id)
            else:
                raise  # pragma: no cover
        self.refresh()
        return resp
