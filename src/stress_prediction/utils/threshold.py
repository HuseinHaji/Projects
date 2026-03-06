from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class ThresholdResult:
    df: pd.DataFrame
    metadata: dict[str, Any]


def add_future_window_stress_label(
    df: pd.DataFrame,
    *,
    vol_col: str,
    split_col: str,
    out_col: str,
    quantile: float,
    horizon_days: int,
    window_days: int,
) -> ThresholdResult:
    """Create a binary stress label using future volatility.

    Purpose
    -------
    Label each observation at time t as stress (1) if the average volatility
    in a future window exceeds a threshold computed from the training sample.

    The future window starts at t + horizon_days and spans window_days.

    Inputs
    ------
    df: DataFrame containing date, volatility, and split columns.
    vol_col: Column containing the volatility measure.
    split_col: Column identifying the dataset split ("train", "test", etc.).
    out_col: Name of the output column for the stress label.
    quantile: Quantile used to compute the stress threshold.
    horizon_days: Number of days ahead before the window begins.
    window_days: Length of the future averaging window.

    Outputs
    -------
    ThresholdResult containing:
    - DataFrame with the new label column.
    - Metadata describing the threshold and labeling parameters.

    Assumptions
    -----------
    - Data contain a "date" column and can be sorted chronologically.
    - Training rows are marked with split_col == "train".

    Failure modes
    -------------
    - ValueError if no training rows are found.
    """
    df = df.sort_values("date").reset_index(drop=True).copy()

    train_mask = df[split_col].eq("train")
    if not train_mask.any():
        raise ValueError("No train rows found when computing stress threshold.")

    threshold = float(df.loc[train_mask, vol_col].quantile(quantile))

    shifted = df[vol_col].shift(-horizon_days)
    future_mean = shifted.rolling(window_days).mean().shift(-(window_days - 1))

    df[out_col] = (future_mean > threshold).astype(int)

    meta: dict[str, Any] = {
        "threshold": threshold,
        "quantile": float(quantile),
        "horizon_days": int(horizon_days),
        "window_days": int(window_days),
        "definition": "stress[t] = 1{ mean(vol[t+h : t+h+w-1]) > threshold(train, q) }",
    }
    return ThresholdResult(df=df, metadata=meta)

def compute_train_threshold(
    df: pd.DataFrame,
    *,
    split_col: str,
    vol_col: str,
    quantile: float,
) -> float:
    """Compute the stress threshold from the training sample.

    Purpose
    -------
    Estimate the volatility threshold used for stress labeling based only on
    the training subset.

    Inputs
    ------
    df: DataFrame containing volatility and split columns.
    split_col: Column identifying the dataset split.
    vol_col: Column containing the volatility measure.
    quantile: Quantile used to compute the threshold.

    Outputs
    -------
    Threshold value as a float.

    Failure modes
    -------------
    - ValueError if no training rows are found.
    """
    train_mask = df[split_col].eq("train")
    if not train_mask.any():
        raise ValueError("No train rows found when computing threshold.")
    return float(df.loc[train_mask, vol_col].quantile(quantile))