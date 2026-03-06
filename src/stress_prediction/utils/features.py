"""Feature engineering for volatility regime monitoring.

Purpose
-------
Generate interpretable time-series features:
- daily returns (log returns)
- rolling volatility of returns (windowed standard deviation)
- lagged features for short-memory dynamics

Inputs
------
- Cleaned DataFrame with columns: date, close.

Outputs
-------
- DataFrame with added columns for returns, volatility, and lags.

Assumptions
-----------
- close is positive.
- dates are sorted.

Failure modes
-------------
- ValueError for missing columns or invalid parameters.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_returns(df: pd.DataFrame, *, close_col: str = "close", out_col: str = "return") -> pd.DataFrame:
    """Add log returns.

    Inputs
    ------
    df: DataFrame containing close prices.
    close_col: Column name for close prices.
    out_col: Output column name for returns.

    Outputs
    -------
    Copy of df with an added out_col.

    Failure modes
    -------------
    - ValueError if close_col missing or contains non-positive values.
    """
    if close_col not in df.columns:
        raise ValueError(f"Missing close column: {close_col}")
    if (df[close_col] <= 0).any():
        raise ValueError("Close prices must be positive to compute log returns")

    out = df.copy()
    out[out_col] = np.log(out[close_col]).diff()
    return out


def add_rolling_volatility(
    df: pd.DataFrame,
    *,
    return_col: str = "return",
    out_col: str = "volatility",
    window_days: int = 21,
) -> pd.DataFrame:
    """Add rolling volatility as rolling std of returns.

    Inputs
    ------
    df: DataFrame with returns.
    return_col: Column name for returns.
    out_col: Output column name for volatility.
    window_days: Rolling window length.

    Outputs
    -------
    Copy of df with an added out_col.

    Failure modes
    -------------
    - ValueError if return_col missing or window_days < 2.
    """
    if return_col not in df.columns:
        raise ValueError(f"Missing return column: {return_col}")
    if window_days < 2:
        raise ValueError("window_days must be at least 2")

    out = df.copy()
    out[out_col] = out[return_col].rolling(window=window_days, min_periods=window_days).std()
    return out


def add_lags(df: pd.DataFrame, *, cols: list[str], max_lag: int) -> pd.DataFrame:
    """Add lagged versions of selected columns.

    Inputs
    ------
    df: DataFrame.
    cols: Column names to lag.
    max_lag: Maximum lag (positive integer).

    Outputs
    -------
    Copy of df with lag columns added: {col}_lag{k}.

    Failure modes
    -------------
    - ValueError if any col missing or max_lag < 1.
    """
    if max_lag < 1:
        raise ValueError("max_lag must be at least 1")
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns for lagging: {missing}")

    out = df.copy()
    for c in cols:
        for k in range(1, max_lag + 1):
            out[f"{c}_lag{k}"] = out[c].shift(k)
    return out