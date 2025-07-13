# Yahoo Finance Microservice

This project provides a simple FastAPI microservice that serves Yahoo Finance price history for a given ticker.

## Requirements

- Python 3.12

Create a virtual environment and install dependencies:

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the service

```bash
uvicorn app.main:app --reload
```

Then visit `http://localhost:8000/history/MSFT` to fetch Microsoft stock history for the last year.

The `/history/{symbol}` endpoint accepts optional query parameters:

* `period` - history period accepted by Yahoo Finance (default `1y`)
* `include_dividends` - set to `true` to include dividend data
* `include_splits` - set to `true` to include stock split data

Dividends and split columns are omitted by default.

Example fetching the last month of data and including dividends:

```bash
curl "http://localhost:8000/history/MSFT?period=1mo&include_dividends=true"
```

Example including both dividends and splits:

```bash
curl "http://localhost:8000/history/MSFT?period=1mo&include_dividends=true&include_splits=true"
```

## Running tests

```bash
pytest
```
