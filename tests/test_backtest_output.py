from __future__ import annotations

import pandas as pd

from stress_prediction.utils.config import project_paths


def test_backtest_predictions_exist_and_valid() -> None:
    paths = project_paths()
    pred_path = paths.predictions_parquet

    df = pd.read_parquet(pred_path)

    assert {"date", "y_true", "proba", "split"} <= set(df.columns)

    assert len(df) > 0
    assert df["proba"].between(0.0, 1.0).all()

    assert set(df["y_true"].unique()).issubset({0, 1})

    assert (df["split"] == "test").all()

    dates = pd.to_datetime(df["date"])
    assert dates.is_monotonic_increasing
