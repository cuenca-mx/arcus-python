from typing import Union

from .base import Resource


class Transaction(Resource):
    _endpoint = '/transactions'

    @classmethod
    def get(cls, transaction_id: Union[int, str]):
        transaction_dict = (
            cls._client.get(f'{cls._endpoint}?q[id_eq]={transaction_id}'))
        return Transaction(**transaction_dict['transactions'][0])

    def cancel(self) -> dict:
        return self._client.post('/transaction/cancel', dict(id=self.id))
