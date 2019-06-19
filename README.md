# Car Parks API

This returns a list of carparks given various filters and paging.

## Requirements

* Python 3.6+ is required 
* PostgreSQL 9.2+ is required

At the moment Postgres server is expected at port 5432, with username "postgres", and password root "root", with empty DB named "postgres". These settings can all be modified in `settings.py` 

## Installation

In project root:
```
pip install -r requirements.txt
```

In `simplewebapi` folder:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## Usage

1. Navigate to `http://localhost:8000/admin`
2. Enter superuser name and password (created above)
3. Use interface to generate and record new API key for use with API
4. API can be accessed using GET from
`http://localhost:8000/carparks/` 
To authenticate the following header must be present in the GET:
`Authorization: Api-Key [API KEY HERE]`

## Features

* The system automatically pages 20 entries per page. Users can filter using any items in the original JSON, e.g.:
`/carparks/?park_and_ride=true`
* Some throttling is implemented - each API key is only allowed 100 requests in a 24 hour period. Will return 429 error until end of period.

## Tests

Tests can be run with:
```python manage.py test```

## Notes

I'd check the technique I've used for filtering features before putting into production as does involve putting user supplied data into a query. If this was a problem could be mitigated by checking the data against a list of known keys in the `feature` field.
