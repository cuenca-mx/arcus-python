import datetime
from dataclasses import dataclass, field
from typing import ClassVar, Optional

from ..exc import UnprocessableEntity, raise_arcus_exception
from .base import Resource

"""
Some of Arcus's billers don't support the new API version 3.1, which is why we
have to use 1.6, the older version instead.
"""
OLD_API_VERSION = '1.6'


@dataclass
class BillPayment(Resource):
    _endpoint: ClassVar[str] = '/bill/pay'

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
        name_on_account: Optional[str] = None,
        topup: bool = False,  # if True, the topup creds will be used
    ):
        if not isinstance(amount, float):
            raise TypeError('amount must be a float')
        data = dict(
            biller_id=biller_id,
            account_number=account_number,
            amount=amount,
            currency=currency,
            name_on_account=name_on_account,
        )
        try:
            bill_payment_dict = cls._client.post(
                cls._endpoint, data, api_version=OLD_API_VERSION, topup=topup
            )
        except UnprocessableEntity as ex:
            raise_arcus_exception(ex, account_number, biller_id, amount)
        return BillPayment(**bill_payment_dict)

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
            f'supported by the API.'
        )
