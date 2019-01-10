from pydash import filter_

from .base import Resource


ENDPOINTS = ['credentials', 'topups', 'utilities']


class Biller(Resource):
    _endpoint = '/billers'

    @classmethod
    def get(cls, _):
        raise NotImplementedError(
            f"{cls.__name__}.get() hasn't been implemented or isn't "
            f"supported by the API."
        )

    @classmethod
    def list(cls, **filters):
        billers = []
        for endpoint in ENDPOINTS:
            billers.extend(cls._list_for_endpoint(endpoint))
        filtered_billers = [Biller(**biller_dict)
                            for biller_dict in filter_(billers, filters)]
        return filtered_billers

    @classmethod
    def _list_for_endpoint(cls, endpoint: str) -> list:
        page = 1
        billers = []
        while True:
            resp = cls._client.get(f'{cls._endpoint}/{endpoint}?page={page}')
            billers.extend(resp['billers'])
            if len(resp['billers']) == 0:
                break
            page += 1
        return billers
