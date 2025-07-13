from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI(title="Yahoo Finance History Service")

@app.get("/")
async def root():
    return {"message": "Yahoo Finance microservice"}

@app.get("/history/{symbol}")
async def get_history(
    symbol: str,
    period: str = "1y",
    include_dividends: bool = False,
    include_splits: bool = False,
):
    """Return historical price data for ``symbol``.

    Parameters
    ----------
    symbol: stock ticker symbol
    period: history period accepted by yfinance (default "1y")
    include_dividends: whether to include the ``Dividends`` column
    include_splits: whether to include the ``Stock Splits`` column
    """
    try:
        data = yf.Ticker(symbol).history(period=period)
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
