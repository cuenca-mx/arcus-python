from .base import Resource


TOPUP_API_VERSION = '1.6'


class Topup(Resource):

    @classmethod
    def create(cls, biller_id: int, account_number: str, amount: float):
        data = dict(biller_id=biller_id,
                    account_number=account_number,
                    amount=amount,
                    currency='MXN')
        topup_dict = cls._client.post('/bill/pay',
                                      data,
                                      api_version=TOPUP_API_VERSION)
        return Topup(**topup_dict)
