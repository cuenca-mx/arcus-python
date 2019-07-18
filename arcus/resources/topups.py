import datetime
from dataclasses import dataclass, field
from typing import Optional

from .base import Resource

"""
Arcus API version 1.6 should be used in order to make top-up operations.
It's because newer API versions don't support this kind of operations.
https://www.arcusfi.com/api/v1_6/#pay
"""
TOPUP_API_VERSION = '1.6'


@dataclass
class Topup(Resource):

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
        data = dict(biller_id=biller_id,
                    account_number=account_number,
                    amount=amount,
                    currency=currency,
                    name_on_account=name_on_account)
        topup_dict = cls._client.post(
            '/bill/pay', data, api_version=TOPUP_API_VERSION)
        return Topup(**topup_dict)

    @classmethod
    def list(cls):
        raise NotImplementedError(
            f"{cls.__name__}.list() hasn't been implemented or isn't "
            f"supported by the API.")
