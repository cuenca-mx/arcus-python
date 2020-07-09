from dataclasses import dataclass, field
from typing import List, Optional, Union

from pydash import filter_

from ..exc import NotFound
from .base import Resource

ENDPOINTS = ['topups', 'utilities']


@dataclass
class Biller(Resource):
    _endpoint = '/billers'

    id: int
    name: str
    country: str
    currency: str
    biller_type: str
    bill_type: str
    hours_to_fulfill: Optional[int] = None
    mask: Optional[str] = None
    account_number_digits: Optional[int] = None
    supports_partial_payments: bool = False
    requires_name_on_account: bool = False
    can_check_balance: bool = False
    required_parameters: List[str] = field(default_factory=list)
    returned_parameters: List[str] = field(default_factory=list)
    can_migrate: bool = field(default=False, repr=False)
    has_xdata: bool = field(default=False, repr=False)
    available_topup_amounts: Optional[list] = None
    topup_fxrate: Optional[float] = None
    topup_commission: Optional[float] = None

    @classmethod
    def get(cls, biller_id: Union[int, str]):
        billers = cls.list(id=int(biller_id))
        if not billers:
            raise NotFound(f'There is no biller with id {biller_id}')
        return billers[0]

    @classmethod
    def list(cls, **filters):
        billers = []
        for endpoint in ENDPOINTS:
            billers.extend(cls._list_for_endpoint(endpoint))
        filtered_billers = [
            Biller(**biller_dict) for biller_dict in filter_(billers, filters)
        ]
        return filtered_billers

    @classmethod
    def _list_for_endpoint(cls, endpoint: str) -> List:
        page = 1
        billers: List[Biller] = []
        while True:
            resp = cls._client.get(f'{cls._endpoint}/{endpoint}?page={page}')
            billers.extend(resp['billers'])
            if len(resp['billers']) == 0:
                break
            page += 1
        return billers
