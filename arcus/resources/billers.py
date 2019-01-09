from pydash import filter_, union

from .base import Resource

ENDPOINTS = ['utilities', 'topups', 'credentials']


class Biller(Resource):

    @classmethod
    def list(
            cls,
            country: str = 'MX',
            currency: str = 'MXN',
            **kwargs
    ):
        billers_list = []
        for endpoint in ENDPOINTS:
            billers = cls.list_billers(endpoint)
            billers_list = union(billers_list, billers)

        filtered_billers_list = filter_(
            billers_list,
            {'country': country,
             'currency': currency}
        )

        return filtered_billers_list

    @classmethod
    def list_billers(cls, endpoint):
        page = 1
        billers = []

        while True:
            resp = cls._client.get(f'/billers/{endpoint}?page={page}')
            billers = union(billers, resp['billers'])

            if len(resp['billers']) == 0:
                break
            page += 1

        return billers
