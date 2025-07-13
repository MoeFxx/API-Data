from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import yfinance as yf
import mplfinance as mpf
import io

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


@app.get("/history/chart")
async def get_history_chart(
    symbol: str,
    timeframe: str = "1y",
    start: Optional[date] = None,
    end: Optional[date] = None,
    include_dividends: bool = False,
    include_splits: bool = False,
):
    """Return a candlestick chart PNG for ``symbol``."""
    try:
        data = yf.Ticker(symbol).history(
            period=timeframe,
            start=start,
            end=end,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    drop_cols = []
    if not include_dividends and "Dividends" in data.columns:
        drop_cols.append("Dividends")
    if not include_splits and "Stock Splits" in data.columns:
        drop_cols.append("Stock Splits")
    if drop_cols:
        data = data.drop(columns=drop_cols)

    buf = io.BytesIO()
    mpf.plot(
        data,
        type="candle",
        style="yahoo",
        volume=True,
        figsize=(16, 9),
        savefig={"fname": buf, "dpi": 120, "bbox_inches": "tight"},
    )
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/png")
