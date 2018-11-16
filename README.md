# arcus-python
[![Build Status](https://travis-ci.com/cuenca-mx/arcus-python.svg?branch=master)](https://travis-ci.com/cuenca-mx/arcus-python)
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

## Simple demo

Current version support direct endpoint calls.

```python
from arcus.client import Client

# Create an Arcus client instance
client = Client('your-api-key', 'your-secret-key', sandbox=True)

# Get account info 
account_info = client.get('/account')

# create bill 
account_info = dict(biller_id=40, account_number='501000000007')
bill = client.post('/bills', account_info)

```


## Release to PyPi

1. Update version in `setup.py`
1. Commit changes to `setup.py` and push to `origin/master`
1. `git tag -a <version> -m <release message>`
1. `git push origin --tags`

TravisCI will release the updated version to PyPi after verifying the tests
pass.
