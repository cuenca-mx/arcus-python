from pydash import filter_

from .base import Resource

ENDPOINTS = ['utilities', 'topups', 'credentials']


class Biller(Resource):

    @classmethod
    def list(cls, **kwargs):
        billers_list = []
        for endpoint in ENDPOINTS:
            billers_list.extend(cls.list_billers(endpoint))
        billers = [Biller(**biller_dict)
                   for biller_dict in filter_(billers_list, kwargs)]
        return billers

    @classmethod
    def list_billers(cls, endpoint: str) -> list:
        page = 1
        billers = []
        while True:
            resp = cls._client.get(f'/billers/{endpoint}?page={page}')
            billers.extend(resp['billers'])
            if len(resp['billers']) == 0:
                break
            page += 1
        return billers
