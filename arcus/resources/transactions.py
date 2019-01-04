from typing import Union

from .base import Resource


class Transaction(Resource):
    _endpoint = '/transactions'

    def __init__(
            self,
            id: int,
            amount: float,
            amount_currency: str,
            status: str,
            **kwargs
    ):
        self.id = id
        self.amount = amount
        self.amount_currency = amount_currency
        self.status = status
        super().__init__(**kwargs)

    @classmethod
    def get(cls, transaction_id: Union[int, str]):
        transaction_dict = (
            cls._client.get(f'{cls._endpoint}?q[id_eq]={transaction_id}'))
        return Transaction(**transaction_dict['transactions'][0])

    def cancel(self) -> dict:
        return self._client.post('/transaction/cancel', dict(id=self.id))
