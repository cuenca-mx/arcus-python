import iso8601


class Resource:
    _client = None
    _endpoint = None

    def __init__(self, **attrs):
        for attr, value in attrs.items():
            if attr.endswith('_at') and value:
                value = iso8601.parse_date(value)
            elif attr.endswith('_date') and value:
                value = iso8601.parse_date(value).date()
            elif attr == 'type':
                continue
            setattr(self, attr, value)

    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def __repr__(self):
        indent = ' ' * 4
        rv = f'{self.__class__.__name__}(\n'
        rv += ',\n'.join([
            f'{indent}{attr}={repr(value)}'
            for attr, value in self.__dict__.items()])
        rv += '\n)'
        return rv

    def __str__(self):
        rv = f'{self.__class__.__name__}('
        rv += ', '.join([
            f'{attr}={repr(value)}'
            for attr, value in self.__dict__.items()])
        rv += ')'
        return rv

    @classmethod
    def get(cls, obj_id):
        obj_dict = cls._client.get(f'{cls._endpoint}/{obj_id}')
        return cls(**obj_dict)

    @classmethod
    def list(cls) -> list:
        type_ = cls._endpoint[1:]
        obj_dicts = cls._client.get(cls._endpoint)[type_]
        objs = [cls(**obj_dict) for obj_dict in obj_dicts]
        return objs
