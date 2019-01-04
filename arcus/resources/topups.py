from .base import Resource


"""
Arcus API version 1.6 should be used in order to make top-up operations.
It's because newer API versions don't support this kind of operations.
https://www.arcusfi.com/api/v1_6/#pay
"""
TOPUP_API_VERSION = '1.6'


class Topup(Resource):

    @classmethod
    def create(
            cls,
            biller_id: int,
            account_number: str,
            amount: float,
            currency: str = 'MXN'
    ):
        data = dict(biller_id=biller_id,
                    account_number=account_number,
                    amount=amount,
                    currency=currency)
        topup_dict = cls._client.post(
            '/bill/pay', data, api_version=TOPUP_API_VERSION)
        return Topup(**topup_dict)

    @classmethod
    def list(cls):
        raise NotImplementedError(
            f"{cls.__class__}.list() hasn't been implemented")
