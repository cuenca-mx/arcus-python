from dataclasses import dataclass


@dataclass
class ApiKey:
    user: str
    secret: str

    def __post_init__(self):
        if not (self.user and self.secret):
            raise ValueError('user and secret must both be defined')
