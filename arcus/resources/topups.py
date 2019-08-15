import datetime
from dataclasses import dataclass, field
from typing import Optional

from arcus.exc import InvalidAccountNumber, UnprocessableEntity

from .base import Resource

"""
Arcus API version 1.6 should be used in order to make top-up operations.
It's because newer API versions don't support this kind of operations.
https://www.arcusfi.com/api/v1_6/#pay
"""
TOPUP_API_VERSION = '1.6'


@dataclass
class Topup(Resource):
    _endpoint = '/bill/pay'

    id: int
    biller_id: int
    account_number: str
    bill_amount: float
    bill_amount_currency: str
    created_at: datetime.datetime
    starting_balance: float
    ending_balance: float
    hours_to_fulfill: Optional[int]
    local_currency: str = field(repr=False)
    fx_rate: float = field(repr=False)
    bill_amount_usd: float = field(repr=False)
    bill_amount_chain_currency: float = field(repr=False)
    payment_transaction_fee: float = field(repr=False)
    payment_total_usd: float = field(repr=False)
    payment_total_chain_currency: float = field(repr=False)
    chain_earned: float = field(repr=False)
    chain_paid: float = field(repr=False)
    bill_amount_local_currency: str = field(repr=False)
    ticket_text: Optional[str] = field(repr=False)
    external_id: Optional[int] = field(repr=False)
    sms_text: Optional[str] = field(repr=False)

    @classmethod
    def create(
            cls,
            biller_id: int,
            account_number: str,
            amount: float,
            currency: str = 'MXN',
            name_on_account: Optional[str] = None
    ):
        if not isinstance(amount, float):
            raise TypeError('amount must be a float')
        data = dict(biller_id=biller_id,
                    account_number=account_number,
                    amount=amount,
                    currency=currency,
                    name_on_account=name_on_account)
        try:
            topup_dict = cls._client.post(
                cls._endpoint, data, api_version=TOPUP_API_VERSION)
        except UnprocessableEntity as ex:
            if ex.code in {'R2', 'R5'}:
                raise InvalidAccountNumber(ex.code, account_number, biller_id)
            else:
                raise
        return Topup(**topup_dict)

    @classmethod
    def get(cls, _):
        raise NotImplementedError(
            f'{cls.__name__}.get(id) is unsupported by the API. Use '
            f'Transaction.get(id) instead.'
        )

    @classmethod
    def list(cls):
        raise NotImplementedError(
            f"{cls.__name__}.list() hasn't been implemented or isn't "
            f'supported by the API.')
