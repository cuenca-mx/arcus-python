from typing import ClassVar, List

import iso8601


class Resource:
    _client: ClassVar['arcus.Client']  # type:ignore  # noqa:F821
    _endpoint: ClassVar[str]

    # Just for mypy
    def __init__(self, *_, **__):  # pragma: no cover
        ...  # pragma: no cover

    def __post_init__(self):
        for attr, value in self.__dict__.items():
            if attr.endswith('_at') and value:
                setattr(self, attr, iso8601.parse_date(value))
            elif attr.endswith('_date') and value:
                setattr(self, attr, iso8601.parse_date(value).date())

    @classmethod
    def get(cls, obj_id):
        obj_dict = cls._client.get(f'{cls._endpoint}/{obj_id}')
        return cls(**obj_dict)

    @classmethod
    def list(cls) -> List:
        type_ = cls._endpoint[1:]
        obj_dicts = cls._client.get(cls._endpoint)[type_]
        objs = [cls(**obj_dict) for obj_dict in obj_dicts]
        return objs
