import datetime
from dataclasses import dataclass, field
from typing import Optional, Union

from arcus.exc import (InvalidAccountNumber, InvalidBiller, NotFound,
                       UnprocessableEntity)

from .base import Resource
from .transactions import Transaction


@dataclass
class Bill(Resource):
    _endpoint = '/bills'

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
    migrated_at: Optional[datetime.datetime]
    type: str
    mfa_challenges: list
    address: dict = field(default_factory=dict)
    payment_method: dict = field(default_factory=dict)
    statements: list = field(default_factory=list)
    subordinates: list = field(default_factory=list)
    payments: list = field(default_factory=list)

    @classmethod
    def create(cls, biller_id: Union[int, str], account_number: str):
        data = dict(biller_id=biller_id, account_number=account_number)
        try:
            bill_dict = cls._client.post(cls._endpoint, data)
        except NotFound:
            raise InvalidBiller(biller_id)
        except UnprocessableEntity as ex:
            if ex.code == 'R2':
                raise InvalidAccountNumber(account_number)
            else:
                raise
        return cls(**bill_dict)

    def pay(self, amount: Optional[float] = None) -> Transaction:
        amount = amount or self.balance
        if not amount:
            raise ValueError('amount is not specified')
        data = dict(amount=amount, currency=self.balance_currency)
        transaction_dict = self._client.post(
            f'{self._endpoint}/{self.id}/pay', data)
        return Transaction(**transaction_dict)
