from __future__ import annotations

import numpy as np
import pandas as pd

from stress_prediction.utils.model import (
    select_model_features,
    train_logistic_regression,
)


def test_train_logreg_and_predict_proba_smoke() -> None:
    n = 400
    df = pd.DataFrame(
        {
            "date": pd.date_range("2020-01-01", periods=n, freq="D"),
            "split": ["train"] * 320 + ["test"] * 80,
            "return": np.linspace(-0.02, 0.02, n),
            "volatility": np.linspace(0.01, 0.05, n),
        }
    )

    for k in range(1, 4):
        df[f"return_lag{k}"] = df["return"].shift(k).bfill()
        df[f"volatility_lag{k}"] = df["volatility"].shift(k).bfill()

    threshold = float(df.loc[df["split"] == "train", "volatility"].quantile(0.8))
    stress_today = (df["volatility"] > threshold).astype(int)
    df["stress"] = stress_today.shift(-1)

    next_split = df["split"].shift(-1)
    df.loc[df["split"] != next_split, "stress"] = np.nan
    df = df.dropna().reset_index(drop=True)
    df["stress"] = df["stress"].astype(int)

    model = train_logistic_regression(df, max_iter=200)
    test_df = df.loc[df["split"] == "test"].copy()

    feature_cols = select_model_features(test_df)
    proba = model.predict_proba(test_df[feature_cols])[:, 1]

    assert proba.shape[0] == len(test_df)
    assert np.isfinite(proba).all()
    assert (proba >= 0).all()
    assert (proba <= 1).all()
