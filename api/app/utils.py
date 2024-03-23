import pandas as pd


def get_stock_tickers(name: str = "", limit: int = 10):
    df = pd.read_csv('./tickers_nasdaq.csv')
    return df[df['Security Name'].str.lower().str.contains(name.lower(), na=False)].head(limit)
