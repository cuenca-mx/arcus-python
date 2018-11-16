from arcus.client import Client


class Transaction:
    def __init__(self, client: Client, transaction_id: int):
        self.client = client
        self.transaction_id = transaction_id

    def show_single(self, transaction_id: int):
        return self.client.get(f'/transactions?q[id_eq]={transaction_id}')

    def cancel(self):
        return self.client.post('/transaction/cancel',
                                dict(id=self.transaction_id))
