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

The microservice always returns one year of historical data for the requested ticker.

## Running tests

```bash
pytest
```
