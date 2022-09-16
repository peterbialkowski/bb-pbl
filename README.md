# Pay By Link

Code examples to stand in for postback functionality in the PayByLink API

## Setup

Requires Python 3.10 (should work on earlier versions but has not been tested)

Create virtual environment and install dependencies

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

or 

globally install dependencies `pip install aiohttp python-dotenv`

## Environment

`cp .env-example .env`

Provide your API Key, Division UUID and a Postback URL

## Example usage

### `monitor.py`

`python3 monitor.py 09ce4312-9160-4101-b9cb-5bd7d1d9a688`

Will poll `/transactions/09ce4312-9160-4101-b9cb-5bd7d1d9a688` every 30 seconds until the payment status is `received` or `cancelled`, then forward the payload to the postback url and terminate the process.

### `transactions.py`

This can be used to monitor all transactions for a given division uuid. Using some logic to check the ecommerce platform for the last known payment status and sending updates to a postback url when the status changes.