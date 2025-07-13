from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI(title="Yahoo Finance History Service")

@app.get("/")
async def root():
    return {"message": "Yahoo Finance microservice"}

@app.get("/history/{symbol}")
async def get_history(symbol: str):
    """Return 1-year historical price data for ``symbol``."""
    try:
        data = yf.Ticker(symbol).history(period="1y")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return data.reset_index().to_dict(orient="records")
