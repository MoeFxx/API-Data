import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Yahoo Finance")

def test_history_params(monkeypatch):


def test_history(monkeypatch):
    import pandas as pd
    import yfinance as yf

    called = {}
    df = pd.DataFrame(
        {
            "Date": [pd.Timestamp("2024-01-01")],
            "Close": [1],
            "Dividends": [0],
            "Stock Splits": [0],
        }
    ).set_index("Date")

    class DummyTicker:
        def history(self, period="1y", start=None, end=None):
            called["period"] = period
            called["start"] = start
            called["end"] = end



    df = pd.DataFrame({"Date": [pd.Timestamp("2024-01-01")], "Close": [1]}).set_index("Date")

    class DummyTicker:
        def history(self, period="1y"):
            called["period"] = period
            return df

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker())

    response = client.get(
        "/history",
        params={
            "symbol": "TEST",
            "timeframe": "1mo",
            "start": "2024-01-01",
            "end": "2024-01-31",
        },
    )
    assert response.status_code == 200
    assert called["period"] == "1mo"
    assert str(called["start"]) == "2024-01-01"
    assert str(called["end"]) == "2024-01-31"
    data = response.json()
    assert "Dividends" not in data[0]
    assert "Stock Splits" not in data[0]
    assert data[0]["Close"] == 1


def test_history_include_extras(monkeypatch):
    import pandas as pd
    import yfinance as yf

    df = pd.DataFrame(
        {
            "Date": [pd.Timestamp("2024-01-01")],
            "Close": [1],
            "Dividends": [0.5],
            "Stock Splits": [2],
        }
    ).set_index("Date")

    class DummyTicker:
        def history(self, period="1y", start=None, end=None):
            return df

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker())

    response = client.get(
        "/history",
        params={
            "symbol": "TEST",
            "include_dividends": "true",
            "include_splits": "true",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["Dividends"] == 0.5
    assert data[0]["Stock Splits"] == 2


def test_history_chart(monkeypatch):
    import pandas as pd
    import yfinance as yf
    import mplfinance as mpf

    df = pd.DataFrame(
        {
            "Date": [pd.Timestamp("2024-01-01")],
            "Open": [1],
            "High": [2],
            "Low": [0.5],
            "Close": [1.5],
            "Volume": [100],
            "Dividends": [0],
            "Stock Splits": [0],
        }
    ).set_index("Date")

    class DummyTicker:
        def history(self, period="1y", start=None, end=None):
            return df

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker())

    def dummy_plot(data, *args, **kwargs):
        savefig = kwargs.get("savefig")
        if isinstance(savefig, dict):
            save_target = savefig.get("fname")
        else:
            save_target = savefig
        if hasattr(save_target, "write"):
            save_target.write(b"img")
=======
    def dummy_plot(data, type="candle", style="charles", volume=True, savefig=None):
        if savefig is not None:
            savefig.write(b"img")

    monkeypatch.setattr(mpf, "plot", dummy_plot)

    response = client.get("/history/chart", params={"symbol": "TEST"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content == b"img"



    response = client.get("/history/TEST")
    assert response.status_code == 200
    assert called["period"] == "1y"
    data = response.json()
    assert data[0]["Close"] == 1

