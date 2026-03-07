"""Run expanding-window backtest and write test-set predictions.

Purpose
-------
Perform an expanding-window backtest with periodic refitting and generate
out-of-sample predicted probabilities for the test period.

Inputs
------
- bld/data/features/spx_features.parquet

Outputs
-------
- bld/data/predictions/predictions.parquet

Assumptions
-----------
- 'split' marks the test period.
- The backtest function refits at a fixed frequency (monthly by default).
- Feature columns exist and contain no leakage (state variables are lagged).

Failure modes
-------------
- Missing feature columns.
- No test rows or no overlap between train history and test blocks.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression

from stress_prediction.utils.backtest import expanding_window_predict_proba
from stress_prediction.utils.config import FEATURES, MODEL, project_paths


def task_backtest_predictions(
    depends_on: Path = project_paths().features_parquet,
    produces: Path = project_paths().predictions_parquet,
) -> None:
    """Generate expanding-window test predictions and write them to parquet.

    Parameters
    ----------
    depends_on:
        Features parquet dataset.
    produces:
        Predictions parquet dataset.
    """
    df = pd.read_parquet(depends_on)

    feature_cols = [
        FEATURES.return_col,
        "vol_21",
        "vol_63",
        "downside_21",
        "skew_63",
        "drawdown_63",
    ] + [c for c in df.columns if c.startswith(f"{FEATURES.return_col}_lag")]

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns in features parquet: {missing}")

    base_model = LogisticRegression(
        random_state=MODEL.random_state,
        max_iter=MODEL.max_iter,
        solver=MODEL.solver,
    )

    res = expanding_window_predict_proba(
        df,
        model=base_model,
        date_col="date",
        feature_cols=feature_cols,
        label_col=FEATURES.label_col,
        split_col=FEATURES.split_col,
        refit_freq="MS",
    )

    produces.parent.mkdir(parents=True, exist_ok=True)
    res.df_pred.to_parquet(produces, index=False)