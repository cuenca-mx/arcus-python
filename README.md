# arcus-python
[![Build Status](https://travis-ci.com/cuenca-mx/arcus-python.svg?branch=master)](https://travis-ci.com/cuenca-mx/arcus-python)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/arcus-python/badge.svg?branch=master)](https://coveralls.io/github/cuenca-mx/arcus-python?branch=master)
[![PyPI](https://img.shields.io/pypi/v/arcus.svg)](https://pypi.org/project/arcus/)


Arcus python3.6 + 3.7 client library for API version 3.1 of [Arcus](https://www.arcusfi.com/).



## Installation and configuration

Create a virtual enviroment an activate it
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate

```

Install arcus
```bash
(venv)$ pip install arcus
```


## Testing
```bash
$ make test
```

## Authentication and account info

Current version support direct endpoint calls.

```python
from arcus.client import Client

# Create an Arcus client instance
client = Client('your-api-key', 'your-secret-key')

# Get account info 
account_info = client.get('/account')

# create bill 
account_info = dict(biller_id=40, account_number='501000000007')
bill = client.post('/bills', account_info)

```

For test purpose you need to add an extra parameter when a client is created

```bash
client = Client('your-api-key', 'your-secret-key', True)
```


## Pay bills

```python
from arcus import Client

client = Client('your-api-key', 'your-secret-key')


# create bill
bill = client.bills.create(40, '501000000007')

# pay bill
transaction = bill.pay()

# show transaction
transaction = client.transactions.get(transaction.id)

# cancel transaction
cancellation = transaction.cancel()
assert cancellation['code'] == 'R0'
assert cancellation['message'] == 'Transaction successful'

# verify cancellation
updated_transaction = client.transactions.get(transaction.id)
assert updated_transaction.id == transaction.id
assert updated_transaction.status == 'refunded'
```

## Top-up
```python
from arcus import Client

client = Client('your-api-key', 'your-secret-key')

biller_id = 808080
phone_number = '5599992222'
amount = 100.0

# by default, currency is MXN
topup = client.topups.create(biller_id, phone_number, amount)

assert topup.bill_amount == 100.0

```

## Release to PyPi

1. Update version in `setup.py`
1. Commit changes to `setup.py` and push to `origin/master`
1. `git tag -a <version> -m <release message>`
1. `git push origin --tags`

TravisCI will release the updated version to PyPi after verifying the tests
pass.
