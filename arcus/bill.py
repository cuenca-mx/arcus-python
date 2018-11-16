from arcus.client import Client


class Bill:
    def __init__(self, client: Client, bill_id: int = None):
        self.client = client
        self.bill_id = bill_id

    def create_bill(self, biller_id: int, account_number: str) -> dict:
        account_info = dict(biller_id=biller_id, account_number=account_number)
        return self.client.post('/bills', account_info)

    def pay(self, amount: float, currency: str) -> dict:
        balance_info = dict(amount=amount, currency=currency)
        return self.client.post(f'/bills/{self.bill_id}/pay', balance_info)
