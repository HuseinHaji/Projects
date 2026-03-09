from __future__ import annotations

import pandas as pd

from stress_prediction.utils.threshold import compute_train_threshold

MAX_EXPECTED_THRESHOLD = 10.0


def test_threshold_uses_train_only() -> None:
    df = pd.DataFrame(
        {
            "date": pd.date_range("2020-01-01", periods=6, freq="D"),
            "split": ["train", "train", "train", "test", "test", "test"],
            "volatility": [1.0, 1.1, 1.2, 100.0, 101.0, 102.0],
        }
    )

    thr = compute_train_threshold(
        df, vol_col="volatility", split_col="split", quantile=0.9
    )

    assert thr < MAX_EXPECTED_THRESHOLD
