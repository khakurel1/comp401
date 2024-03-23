from fastapi import APIRouter
from app.utils import get_stock_tickers

router = APIRouter(
    prefix="/tickers",
    tags=["tickers"]
)


class Ticker:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol


@router.get("/")
def ticker_index(name: str, limit: int = 10):
    res = get_stock_tickers(name, limit)

    tickers = [Ticker(row['Security Name'], row['Symbol'])
               for _, row in res.iterrows()]

    return {
        "status": "success",
        "tickers": tickers
    }
