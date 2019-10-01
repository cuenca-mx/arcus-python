import datetime
from dataclasses import dataclass, field
from typing import ClassVar, Optional, Union

from arcus.exc import (
    AlreadyPaid,
    DuplicatedPayment,
    IncompleteAmount,
    InvalidAccountNumber,
    InvalidAmount,
    InvalidBiller,
    NotFound,
    RecurrentPayments,
    UnprocessableEntity,
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
            if ex.code in {'R1', 'R2', 'R29'}:
                raise InvalidAccountNumber(ex.code, account_number, biller_id)
            else:
                raise
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
            if ex.code == 'R102':
                raise InvalidAmount(ex.code, ex.message, amount=amount)
            elif ex.code in {'R3', 'R11', 'R41'}:
                raise IncompleteAmount(ex.code, amount=amount)
            elif ex.code == 'R7':
                raise RecurrentPayments(ex.code)
            elif ex.code == 'R36':
                raise DuplicatedPayment(ex.code, amount=amount)
            elif ex.code in {'R12', 'R8'}:
                raise AlreadyPaid(ex.code)
            else:
                raise
        return Transaction(**transaction_dict)
