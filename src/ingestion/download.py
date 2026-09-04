"""
ATLAS — Data Ingestion (Phase 1)

Downloads daily OHLCV data for the asset universe defined in
config/assets.py and aligns everything to trading days only.

Design decision (v0.1): weekends/holidays are dropped entirely, for every
asset, including BTC/ETH. This keeps the dataset honest — no fabricated
prices on days the stock market was closed — at the cost of losing crypto's
weekend-only price movement. Revisit this if/when weekend crypto behavior
becomes its own research question.
"""

import pandas as pd
import yfinance as yf


def download_asset(ticker: str, start: str) -> pd.DataFrame:
    """
    Download raw daily OHLCV data for a single ticker from Yahoo Finance.

    Returns a DataFrame indexed by date, with columns:
    Open, High, Low, Close, Volume  (Close is already split/dividend
    adjusted — yfinance does this for us by default).
    """
    data = yf.download(ticker, start=start, progress=False, auto_adjust=True)

    if data.empty:
        raise ValueError(f"No data returned for {ticker}. Check the symbol.")

    # yfinance sometimes returns multi-level columns even for a single
    # ticker — flatten that so we get plain column names.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def load_market_data(assets: dict, start: str) -> pd.DataFrame:
    """
    Download and align daily closing prices for every asset in `assets`.

    Parameters
    ----------
    assets : dict
        Maps a short label to a yfinance ticker, e.g. {"BTC": "BTC-USD"}.
    start : str
        Start date, "YYYY-MM-DD".

    Returns
    -------
    pd.DataFrame
        One column per asset (using the short label as the column name),
        one row per trading day. Only days present for EVERY asset are
        kept — this is the "weekdays only" alignment decision: since
        stock tickers have no weekend rows to begin with, an inner join
        automatically drops BTC/ETH's weekend rows too.
    """
    closes = {}

    for label, ticker in assets.items():
        raw = download_asset(ticker, start)
        closes[label] = raw["Close"]

    # Combine all series into one table. how="inner" keeps only dates
    # that exist in EVERY series — this is what enforces "weekdays only,"
    # since SPY/QQQ/NVDA/COIN simply have no rows for Sat/Sun to begin
    # with, so the intersection with BTC/ETH's daily rows drops those
    # weekend dates automatically.
    combined = pd.concat(closes, axis=1, join="inner")
    combined.index.name = "Date"

    return combined


if __name__ == "__main__":
    # Quick manual test: run `python -m src.ingestion.download` from the
    # atlas/ root to see this in action.
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from config.assets import ASSETS, DEFAULT_START
    from src.processing.save import save_market_data

    df = load_market_data(ASSETS, DEFAULT_START)
    save_market_data(df)

    from src.processing.save import load_saved_market_data
    from src.analytics.returns import compute_log_returns, correlation_matrix
    from src.processing.validate import print_validation_report

    saved_df = load_saved_market_data()
    log_returns = compute_log_returns(saved_df)
    
    print(df.tail())
    print(f"\nShape: {df.shape}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")

    print("\nCorrelation Matrix: ")
    print(correlation_matrix(log_returns))

    print_validation_report(saved_df)
    

    
