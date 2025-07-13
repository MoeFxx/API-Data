from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI(title="Yahoo Finance History Service")

@app.get("/")
async def root():
    return {"message": "Yahoo Finance microservice"}

@app.get("/history")
async def get_history(
    symbol: str,
    timeframe: str = "1y",
    start: Optional[date] = None,
    end: Optional[date] = None,
    include_dividends: bool = False,
    include_splits: bool = False,
):
    """Return historical price data for ``symbol``.

    Parameters
    ----------
    symbol: Stock ticker symbol
    timeframe: History period accepted by yfinance (default ``"1y"``)
    start: Optional start date in ``YYYY-MM-DD`` format
    end: Optional end date in ``YYYY-MM-DD`` format
    include_dividends: Include the ``Dividends`` column when ``True``
    include_splits: Include the ``Stock Splits`` column when ``True``
    """
    try:
        data = yf.Ticker(symbol).history(
            period=timeframe,
            start=start,
            end=end,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    data = data.reset_index()
    drop_cols = []
    if not include_dividends and "Dividends" in data.columns:
        drop_cols.append("Dividends")
    if not include_splits and "Stock Splits" in data.columns:
        drop_cols.append("Stock Splits")
    if drop_cols:
        data = data.drop(columns=drop_cols)

    return data.to_dict(orient="records")
@app.get("/history/{symbol}")
async def get_history(symbol: str):
    """Return 1-year historical price data for ``symbol``."""
    try:
        data = yf.Ticker(symbol).history(period="1y")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return data.reset_index().to_dict(orient="records")
