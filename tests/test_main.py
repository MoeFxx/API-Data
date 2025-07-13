import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Yahoo Finance")


def test_history_excludes_columns(monkeypatch):
    import pandas as pd
    import yfinance as yf

    df = pd.DataFrame(
        {
            "Date": [pd.Timestamp("2024-01-01")],
            "Open": [1],
            "High": [1],
            "Low": [1],
            "Close": [1],
            "Volume": [1],
            "Dividends": [0.1],
            "Stock Splits": [0],
        }
    ).set_index("Date")

    class DummyTicker:
        def history(self, period="1y"):
            return df

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker())

    response = client.get("/history/TEST")
    assert response.status_code == 200
    data = response.json()[0]
    assert "Dividends" not in data
    assert "Stock Splits" not in data


def test_history_include_columns(monkeypatch):
    import pandas as pd
    import yfinance as yf

    df = pd.DataFrame(
        {
            "Date": [pd.Timestamp("2024-01-01")],
            "Open": [1],
            "High": [1],
            "Low": [1],
            "Close": [1],
            "Volume": [1],
            "Dividends": [0.1],
            "Stock Splits": [0],
        }
    ).set_index("Date")

    class DummyTicker:
        def history(self, period="1y"):
            return df

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker())

    response = client.get("/history/TEST?include_dividends=true&include_splits=true")
    assert response.status_code == 200
    data = response.json()[0]
    assert "Dividends" in data
    assert "Stock Splits" in data

def test_history_custom_period(monkeypatch):
    import pandas as pd
    import yfinance as yf

    called = {}
    df = pd.DataFrame(
        {
            "Date": [pd.Timestamp("2024-01-01")],
            "Open": [1],
            "High": [1],
            "Low": [1],
            "Close": [1],
            "Volume": [1],
        }
    ).set_index("Date")

    class DummyTicker:
        def history(self, period="1y"):
            called["period"] = period
            return df

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker())

    response = client.get("/history/TEST?period=5d")
    assert response.status_code == 200
    assert called["period"] == "5d"
