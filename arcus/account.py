from arcus.client import Client


class Account:
    def __init__(self, client: Client):
        self.client = client

    def get_info(self) -> dict:
        return self.client.get('/account')
