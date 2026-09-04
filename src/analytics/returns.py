"""
ATLAS — Statistics Engine (Phase 2)

Computes returns, volatility, and correlation from the cleaned price
data produced in Phase 1.
"""

import numpy as np
import pandas as pd


def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a table of prices into a table of daily log returns.

    log_return[t] = ln(price[t] / price[t-1])

    The first row will be NaN (there's no "yesterday" for day 1), so we
    drop it.
    """
    log_returns = np.log(prices / prices.shift(1))
    return log_returns.dropna()


def compute_rolling_volatility(returns: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """
    Rolling standard deviation of returns — how bouncy each asset has
    been over the trailing `window` days. Annualized by the usual
    sqrt(252) convention (252 = roughly the number of trading days in a
    year), so the number is comparable across time windows.
    """
    return returns.rolling(window=window).std() * np.sqrt(252)


def compute_rolling_correlation(returns: pd.DataFrame, asset_a: str, asset_b: str, window: int = 30) -> pd.Series:
    """
    Rolling correlation between two assets over the trailing `window`
    days — shows whether their relationship is stable or changing over
    time, instead of collapsing everything into one static number.
    """
    return returns[asset_a].rolling(window=window).corr(returns[asset_b])


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """
    A single, static correlation matrix across all assets — a quick
    snapshot, not the full time-varying picture.
    """
    return returns.corr()

def compute_simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Plain percentage returns: (price[t] - price[t-1]) / price[t-1]

    More intuitive to read/report than log returns, but doesn't stack
    across days as cleanly — kept alongside log returns, not instead of.
    """
    return prices.pct_change().dropna()


def compute_zscores(returns: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """
    Rolling z-score of each day's return: how many standard deviations
    away from its own trailing-window average was that day's move?
    """
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()
    return (returns - rolling_mean) / rolling_std


def compute_drawdown(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage drop from each asset's running peak price so far.
    0 means "at an all-time high right now." -0.30 means "30% below
    the highest price seen up to this point."
    """
    running_max = prices.cummax()
    return (prices - running_max) / running_max
