"""
ATLAS — Data Storage (Phase 1)

Saves a cleaned market-data DataFrame to Parquet so downstream phases
(statistics, lead/lag, etc.) don't need to re-download from Yahoo Finance
on every run.
"""

import os
import pandas as pd


def save_market_data(df: pd.DataFrame, path: str = "data/market_data.parquet") -> None:
    """Save the combined market data table to Parquet."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path)
    print(f"Saved {df.shape[0]} rows x {df.shape[1]} columns to {path}")


def load_saved_market_data(path: str = "data/market_data.parquet") -> pd.DataFrame:
    """Load a previously saved market data table from Parquet."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No saved data at {path}. Run the ingestion script first."
        )
    return pd.read_parquet(path)
    
