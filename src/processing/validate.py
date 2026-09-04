"""
ATLAS — Data Validation (Phase 1)

Sanity-checks a market-data DataFrame after download, before it's
trusted anywhere downstream. This doesn't fix problems — it just
surfaces them loudly so you notice instead of silently computing
statistics on bad data.
"""

import pandas as pd


def validate_market_data(df: pd.DataFrame, max_daily_move: float = 0.5) -> list[str]:
    """
    Run a set of sanity checks on a price DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Prices, one column per asset, indexed by date.
    max_daily_move : float
        Flag any single-day percentage move bigger than this (0.5 = 50%)
        as suspicious. Crypto can legitimately move this much, so this
        is a "look closer," not "this is definitely wrong."

    Returns
    -------
    list[str]
        Human-readable warnings. Empty list means everything looked clean.
    """
    warnings = []

    # 1. Missing values
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        warnings.append(f"Missing values found:\n{missing}")

    # 2. Duplicate dates
    duplicate_dates = df.index[df.index.duplicated()]
    if len(duplicate_dates) > 0:
        warnings.append(f"Duplicate dates found: {list(duplicate_dates)}")

    # 3. Zero or negative prices
    bad_prices = (df <= 0).sum()
    bad_prices = bad_prices[bad_prices > 0]
    if not bad_prices.empty:
        warnings.append(f"Zero/negative prices found:\n{bad_prices}")

    # 4. Suspiciously large single-day moves
    pct_change = df.pct_change().abs()
    big_moves = pct_change[pct_change > max_daily_move]
    big_moves = big_moves.dropna(how="all")
    if not big_moves.empty:
        warnings.append(
            f"Daily moves bigger than {max_daily_move:.0%} found on "
            f"{len(big_moves)} date(s) — inspect before trusting:\n{big_moves.dropna(axis=1, how='all')}"
        )

    return warnings


def print_validation_report(df: pd.DataFrame) -> None:
    """Run validation and print a readable pass/fail report."""
    warnings = validate_market_data(df)
    if not warnings:
        print("✅ Validation passed — no issues found.")
    else:
        print(f"⚠️  Validation found {len(warnings)} issue(s):\n")
        for w in warnings:
            print(w)
            print()
