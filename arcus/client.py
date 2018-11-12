API_VERSION = '3.1'
PRODUCTION_API_URL = 'https://...'
SANDBOX_API_URL = 'https://...'


class Client:

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            sandbox: bool = False,
            api_version: str = API_VERSION
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        if sandbox:
            self.base_url = SANDBOX_API_URL
        else:
            self.base_url = PRODUCTION_API_URL
        self.api_version = api_version

    def get(self, endpoint: str, **kwargs) -> dict:
        return self.request('get', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> dict:
        return self.request('post', endpoint, **kwargs)

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        pass
