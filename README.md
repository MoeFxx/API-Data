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

The service exposes a `/history` endpoint that accepts a stock symbol and
optional query parameters. Example:

```bash
curl 'http://localhost:8000/history?symbol=MSFT&timeframe=6mo&start=2024-01-01&end=2024-06-30'
```

Query parameters:

- `symbol` (required): stock ticker symbol.
- `timeframe` (optional, default `1y`): history period accepted by yfinance.
- `start` / `end` (optional): date range in `YYYY-MM-DD` format.
- `include_dividends` and `include_splits` (optional): include those columns when set to `true`.

The service also provides `/history/chart`, which returns a high-definition candlestick chart as a PNG image using the same query parameters. The chart is rendered in a dark theme and sized for a 1080p resolution.

The service also provides `/history/chart`, which returns a candlestick chart as a PNG image using the same query parameters.


```bash
curl 'http://localhost:8000/history/chart?symbol=MSFT&timeframe=1mo'
```


Then visit `http://localhost:8000/history/MSFT` to fetch Microsoft stock history for the last year.

The microservice always returns one year of historical data for the requested ticker.

## Running tests

```bash
pytest
```
