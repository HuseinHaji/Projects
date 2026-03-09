"""Build features and labels for stress prediction.

Purpose
-------
Create return-based features, lagged state variables, train/test split markers,
and an honest forward-looking stress label based on future realized volatility.

Inputs
------
- bld/data/clean/spx_clean.parquet

Outputs
-------
- bld/data/features/spx_features.parquet
- bld/data/features/threshold.json

Assumptions
-----------
- Stress threshold is computed on TRAIN only (no leakage).
- Label is defined as a future-window average volatility event.
- State variables are shifted by 1 day to avoid look-ahead bias.

Failure modes
-------------
- Missing required columns in the cleaned dataset.
- Insufficient history for rolling windows / lags.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from stress_prediction.utils.config import FEATURES, project_paths
from stress_prediction.utils.features import add_lags, add_returns, add_rolling_volatility
from stress_prediction.utils.split import add_time_split
from stress_prediction.utils.threshold import add_future_window_stress_label
from stress_prediction.utils.utils import write_json


def task_build_features(
    depends_on: Path = project_paths().clean_parquet,
    produces: dict[str, Path] = {
        "features": project_paths().features_parquet,
        "threshold": project_paths().threshold_json,
    },
) -> None:
    """Create the final modeling dataset (features + label) and write outputs.

    Parameters
    ----------
    depends_on:
        Clean parquet input dataset.
    produces:
        Output paths for the features parquet and the threshold metadata JSON.
    """
    df = pd.read_parquet(depends_on)

    df = add_returns(df, close_col="close", out_col=FEATURES.return_col)

    df = add_rolling_volatility(
        df,
        return_col=FEATURES.return_col,
        out_col=FEATURES.vol_col,
        window_days=FEATURES.rolling_window_days,
    )

    df["vol_21"] = df[FEATURES.return_col].rolling(21).std()
    df["vol_63"] = df[FEATURES.return_col].rolling(63).std()

    df["downside_21"] = (df[FEATURES.return_col] < 0).rolling(21).mean()

    df["skew_63"] = df[FEATURES.return_col].rolling(63).skew()

    rolling_max_63 = df["close"].rolling(63).max()
    df["drawdown_63"] = df["close"] / rolling_max_63 - 1.0

    state_cols = ["vol_21", "vol_63", "downside_21", "skew_63", "drawdown_63"]
    df[state_cols] = df[state_cols].shift(1)

    split_res = add_time_split(
        df,
        date_col="date",
        split_col=FEATURES.split_col,
        test_size=FEATURES.test_size,
        min_train_size=FEATURES.min_train_size,
    )
    df = split_res.df

    df = add_lags(df, cols=[FEATURES.return_col], max_lag=FEATURES.lag_days)

    thr_res = add_future_window_stress_label(
        df,
        vol_col=FEATURES.vol_col,
        split_col=FEATURES.split_col,
        out_col=FEATURES.label_col,
        quantile=FEATURES.threshold_quantile,
        horizon_days=10,
        window_days=5,
    )
    df = thr_res.df

    keep_cols = [
        "date",
        "close",
        FEATURES.split_col,
        FEATURES.label_col,
        FEATURES.return_col,
        FEATURES.vol_col,  
        "vol_21",
        "vol_63",
        "downside_21",
        "skew_63",
        "drawdown_63",
    ]
    lag_cols = [c for c in df.columns if c.startswith(f"{FEATURES.return_col}_lag")]

    df = df[keep_cols + sorted(lag_cols)].dropna().reset_index(drop=True)

    produces["features"].parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(produces["features"], index=False)
    write_json(produces["threshold"], thr_res.metadata)