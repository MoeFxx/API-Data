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

def test_history(monkeypatch):
    import pandas as pd
    import yfinance as yf

    called = {}
    df = pd.DataFrame({"Date": [pd.Timestamp("2024-01-01")], "Close": [1]}).set_index("Date")

    class DummyTicker:
        def history(self, period="1y"):
            called["period"] = period
            return df

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker())

    response = client.get("/history/TEST")
    assert response.status_code == 200
    assert called["period"] == "1y"
    data = response.json()
    assert data[0]["Close"] == 1
