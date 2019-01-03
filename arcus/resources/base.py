class Resource:
    _client = None
    _endpoint = None

    def __init__(self, **attrs):
        for attr, value in attrs.items():
            setattr(self, attr, value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        indent = ' ' * 4
        attrs = {}
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                value = f"'{value}'"
            attrs[attr] = value
        rv = f'{self.__class__.__name__}(\n'
        rv += ',\n'.join([
            f'{indent}{attr}={value}'
            for attr, value in attrs.items()])
        rv += '\n)'
        return rv

    def __str__(self):
        attrs = {}
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                value = f"'{value}'"
            attrs[attr] = value
        rv = f'{self.__class__.__name__}('
        rv += ', '.join([
            f'{attr}={value}'
            for attr, value in attrs.items()])
        rv += ')'
        return rv

    @classmethod
    def get(cls, obj_id):
        obj_dict = cls._client.get(f'{cls._endpoint}/{obj_id}')
        return cls(**obj_dict)
