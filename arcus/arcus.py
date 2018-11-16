from arcus.account import Account
from arcus.bill import Bill
from arcus.client import Client
from arcus.transaction import Transaction


class Arcus:
    def __init__(self,
                 api_key: str,
                 secret_key: str,
                 sandbox: bool = False):
        self.client = Client(api_key, secret_key, sandbox)

    def account(self) -> Account:
        return Account(self.client)

    def bills(self, bill_id: int = None) -> Bill:
        return Bill(self.client, bill_id)

    def transaction(self, transaction_id: int = None) -> Transaction:
        return Transaction(self.client, transaction_id)
