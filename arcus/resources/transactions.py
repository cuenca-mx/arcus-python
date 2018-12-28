from typing import Union

from .base import Resource


class Transaction(Resource):
    _endpoint = '/transactions'

    @classmethod
    def cancel(cls, transaction_id: Union[int, str]):
        transaction_data = dict(id=transaction_id)
        transaction_dict = cls._client.post(
            '/transaction/cancel', transaction_data)
        return Transaction(**transaction_dict)

    @classmethod
    def get(cls, transaction_id: Union[int, str]):
        transaction_dict = (
            cls._client.get(f'{cls._endpoint}?q[id_eq]={transaction_id}'))
        return Transaction(**transaction_dict['transactions'][0])
