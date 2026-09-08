"""
ATLAS — Intraday Data Ingestion (Phase 3)

Downloads minute-level data for lead/lag analysis. Unlike daily data,
Yahoo Finance only offers 1-minute candles for roughly the last 7 days,
so this pulls a short recent window, not full history.
"""

import pandas as pd
import yfinance as yf


def download_intraday(ticker: str, period: str = "7d", interval: str = "1m") -> pd.DataFrame:
    """
    Download minute-level OHLCV data for a single ticker.

    Parameters
    ----------
    ticker : str
        yfinance ticker, e.g. "BTC-USD" or "QQQ".
    period : str
        How far back to look. "7d" is close to the max yfinance allows
        for 1-minute data.
    interval : str
        Candle size — "1m" for 1-minute bars.
    """
    data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)

    if data.empty:
        raise ValueError(f"No intraday data returned for {ticker}.")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def align_to_market_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    Restrict a DataFrame's timestamps to US stock market hours
    (9:30am-4:00pm Eastern, weekdays only).

    This is necessary because BTC/ETH trade 24/7 but stocks don't —
    comparing "who moved first" only makes sense during the window
    when BOTH assets are actually trading.
    """
    # yfinance intraday timestamps come back timezone-aware already,
    # usually in US/Eastern for US tickers. Convert to be safe.
    df = df.copy()
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert("US/Eastern")
    else:
        df.index = df.index.tz_convert("US/Eastern")

    market_open = df.index.indexer_between_time("09:30", "16:00")
    df = df.iloc[market_open]

    # Weekdays only (Mon=0 ... Sun=6)
    df = df[df.index.weekday < 5]

    return df


def load_intraday_pair(ticker_a: str, ticker_b: str) -> pd.DataFrame:
    """
    Download and align two tickers' 1-minute closing prices, restricted
    to shared market-open hours, into one combined DataFrame.
    """
    raw_a = download_intraday(ticker_a)
    raw_b = download_intraday(ticker_b)

    aligned_a = align_to_market_hours(raw_a)["Close"]
    aligned_b = align_to_market_hours(raw_b)["Close"]

    combined = pd.concat({ticker_a: aligned_a, ticker_b: aligned_b}, axis=1, join="inner")
    return combined
