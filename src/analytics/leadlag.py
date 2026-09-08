"""
ATLAS — Lead/Lag Engine (Phase 3)

Answers: does one asset's past movement help explain another asset's
current movement, and if so, by how many days?

Day-level version (v0.1). Upgrading to intraday (minute-level) lag is a
future step, once this coarser version proves the approach works.
"""

import pandas as pd
from scipy.stats import pearsonr


def lagged_correlation(returns: pd.DataFrame, leader: str, follower: str, max_lag: int = 5) -> pd.Series:
    """
    Compare `follower`'s returns today against `leader`'s returns from
    1, 2, 3... up to `max_lag` days ago.

    A high correlation at lag=2, for example, means: "follower's return
    today tends to echo what leader did 2 days earlier" — a hint that
    leader's moves show up in follower with a 2-day delay.

    Returns
    -------
    pd.Series
        Index = lag (in days), values = correlation at that lag.
        Read this like a leaderboard: whichever lag has the highest
        correlation is the "best explaining" delay.
    """
    results = {}
    for lag in range(1, max_lag + 1):
        # Shift the leader's returns forward by `lag` days, so that
        # leader's return from `lag` days ago lines up with follower's
        # return today.
        shifted_leader = returns[leader].shift(lag)
        results[lag] = shifted_leader.corr(returns[follower])

    return pd.Series(results, name=f"{leader} (lagged) vs {follower} (today)")

def lagged_correlation_with_significance(returns: pd.DataFrame, leader: str, follower: str, max_lag: int = 10)->pd.DataFrame:
    """
    Same idea as lagged_correlation, but also return a p-value for each lag - telling you whether 
    that correlation is likely a real signal or could plausibly be random chance.

    Rule of Thumb: p < 0.05 means "unlikely to be random noise."
    """
    results = []
    for lag in range(1,max_lag +1):
        shifted_leader = returns[leader].shift(lag)
        # pearsonr can't handle NaN values (the first `lag` rows will be
        # NaN after shifting), so drop rows where either side is missing.
        paired = pd.concat([shifted_leader, returns[follower]], axis=1).dropna()
        
        corr, p_value = pearsonr(paired.iloc[:, 0], paired.iloc[:, 1])
        results.append({"lag": lag, "correlation": corr, "p_value": p_value, "significant": p_value < 0.05})
        
    return pd.DataFrame(results).set_index("lag")

def split_half_validation(returns: pd.DataFrame, leader: str, follower: str, lag: int) -> dict:
    """
    Check whether a specific lag's correlation holds up in both the
    first and second half of the data, independently. A real pattern
    should show up in both halves; a fluke usually won't.
    """
    midpoint = len(returns) // 2
    first_half = returns.iloc[:midpoint]
    second_half = returns.iloc[midpoint:]

    results = {}
    for label, half in [("first_half", first_half), ("second_half", second_half)]:
        shifted_leader = half[leader].shift(lag)
        paired = pd.concat([shifted_leader, half[follower]], axis=1).dropna()
        corr, p_value = pearsonr(paired.iloc[:, 0], paired.iloc[:, 1])
        results[label] = {"correlation": corr, "p_value": p_value, "significant": p_value < 0.05, "n": len(paired)}

    return results
