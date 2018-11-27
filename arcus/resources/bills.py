from .base import Resource
from .transactions import Transaction

ARCUS_API_VERSION_1_6 = '1.6'


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

    @classmethod
    def topup(cls, biller_id: int, account_number: str, amount: float):
        data = dict(biller_id=biller_id,
                    account_number=account_number,
                    amount=amount,
                    currency='MXN')
        topup_dict = cls._client.post('/bill/pay', ARCUS_API_VERSION_1_6, data)
        return Transaction(**topup_dict)
