"""
ATLAS - Visualization (Phase 2)

Simple plotting helpers for correlation and volatility over time.
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_rolling_correlation(corr_series: pd.Series, asset_a: str, asset_b: str, save_path: str = None) -> None:
    """
    Plot a rolling correlation series over time.

    If save_path is given, saves a PNG instead of (or in addition to)
    showing an interactive window - useful since you're on a terminal - heavy workflow
    rather that always having a GUI window handy.
    """
    plt.figure(figsize = (12,5))
    plt.plot(corr_series.index, corr_series.values)
    plt.axhline(0, color = "grey", linestyle="--", linewidth=1)
    plt.title(f"{asset_a} <-> {asset_b} Rolling Correlation  (30 day)")
    plt.xlabel("Date")
    plt.ylabel("Correlation")
    plt.ylim(-1, 1)
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi = 150, bbox_inches="tight")
        print(f"Saved chart to {save_path}")
    else:   
        plt.show()
