import datetime
from dataclasses import dataclass, field
from typing import ClassVar, Optional, Union

from ..exc import (
    InvalidBiller,
    NotFound,
    UnprocessableEntity,
    raise_arcus_exception,
)
from .base import Resource
from .transactions import Transaction


@dataclass
class Bill(Resource):
    _endpoint: ClassVar[str] = '/bills'

    id: int
    biller_id: int
    account_number: str
    balance: Optional[float]
    balance_currency: str
    name_on_account: Optional[str]
    due_date: Optional[datetime.date]
    balance_updated_at: Optional[datetime.datetime]
    error_code: Optional[str]
    error_message: Optional[str]
    status: str
    migrated_at: Optional[datetime.datetime] = field(repr=False)
    type: str = field(repr=False)
    mfa_challenges: list = field(repr=False)
    address: dict = field(default_factory=dict, repr=False)
    payment_method: dict = field(default_factory=dict, repr=False)
    statements: list = field(default_factory=list, repr=False)
    subordinates: list = field(default_factory=list, repr=False)
    payments: list = field(default_factory=list, repr=False)

    @classmethod
    def create(cls, biller_id: Union[int, str], account_number: str):
        data = dict(biller_id=biller_id, account_number=account_number)
        try:
            bill_dict = cls._client.post(cls._endpoint, data)
        except NotFound:
            raise InvalidBiller(biller_id)
        except UnprocessableEntity as ex:
            raise_arcus_exception(ex, account_number, int(biller_id))
        return cls(**bill_dict)

    def pay(self, amount: Optional[float] = None) -> Transaction:
        amount = amount or self.balance
        if not amount:
            raise ValueError('amount is not specified')
        if not isinstance(amount, float):
            raise TypeError('amount must be a float')
        data = dict(amount=amount, currency=self.balance_currency)
        try:
            transaction_dict = self._client.post(
                f'{self._endpoint}/{self.id}/pay', data
            )
        except UnprocessableEntity as ex:
            raise_arcus_exception(
                ex, self.account_number, self.biller_id, amount
            )
        return Transaction(**transaction_dict)
