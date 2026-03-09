from __future__ import annotations

import pandas as pd

from stress_prediction.utils.features import (
    add_lags,
    add_returns,
    add_rolling_volatility,
)
from stress_prediction.utils.split import add_time_split


def test_add_time_split_creates_train_and_test() -> None:
    df = pd.DataFrame(
        {"date": pd.date_range("2020-01-01", periods=300, freq="D"), "close": 100.0}
    )
    res = add_time_split(df, test_size=0.2, min_train_size=200)
    assert "split" in res.df.columns
    assert set(res.df["split"].unique()) == {"train", "test"}
    assert res.df.loc[0, "split"] == "train"
    assert res.df.loc[res.df.shape[0] - 1, "split"] == "test"


def test_core_features_exist_after_generation() -> None:
    df = pd.DataFrame(
        {"date": pd.date_range("2020-01-01", periods=60, freq="D"), "close": 100.0}
    )
    out = add_returns(df)
    out = add_rolling_volatility(out, window_days=21)
    out = add_lags(out, cols=["return", "volatility"], max_lag=3)
    assert "return" in out.columns
    assert "volatility" in out.columns
    assert "return_lag1" in out.columns
    assert "volatility_lag3" in out.columns
