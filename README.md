# arcus-python
[![Build Status](https://travis-ci.com/cuenca-mx/arcus-python.svg?branch=master)](https://travis-ci.com/cuenca-mx/arcus-python)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/arcus-python/badge.svg?branch=master)](https://coveralls.io/github/cuenca-mx/arcus-python?branch=master)
[![PyPI](https://img.shields.io/pypi/v/arcus.svg)](https://pypi.org/project/arcus/)


Arcus python3.6 + 3.7 client library for API version 3.1 of [Arcus](https://www.arcusfi.com/).



## Install

```bash
$ pip install arcus
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


## Pay bills

```python
from arcus import Client

client = Client('your-api-key', 'your-secret-key')


# create bill
bill = client.bills.create(40, '501000000007')

# pay bill
transaction = bill.pay()

# refresh transaction
transaction.refresh()

# cancel transaction
cancellation = transaction.cancel()
assert cancellation['code'] == 'R0'
assert cancellation['message'] == 'Transaction successful'
assert transaction.status == 'refunded'
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


## Billers list

You can list all active billers or filter in a specific field
```python
from arcus.client import Client

# Create an Arcus client instance
client = Client('your-api-key', 'your-secret-key')

# Get all billers in Mexico which use MXN as currency
mx_biller_list = client.biller.list(country='MX', currency='MXN')

# Get all billers with an specific biller_type
electricity_biller_list = client.biller.list(biller_type='Electricity')
