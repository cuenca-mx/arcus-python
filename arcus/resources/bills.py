from .base import Resource
from .transactions import Transaction


class Bill(Resource):
    _endpoint = '/bills'

    @classmethod
    def create(cls, biller_id, account_number):
        data = dict(biller_id=biller_id, account_number=account_number)
        bill_dict = cls._client.post(cls._endpoint, data)
        return cls(**bill_dict)

    def pay(self, amount=None):
        amount = amount or self.balance
        data = dict(amount=amount, currency=self.balance_currency)
        transaction_dict = self._client.post(
            f'{self._endpoint}/{self.id}/pay', data)
        return Transaction(**transaction_dict)
