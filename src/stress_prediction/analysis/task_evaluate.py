"""Compute evaluation metrics from backtest predictions.

Purpose
-------
Compute classification metrics (e.g., AUC) using the test-set predictions
produced by the expanding-window backtest.

Inputs
------
- bld/data/predictions/predictions.parquet

Outputs
-------
- bld/tables/metrics.csv

Assumptions
-----------
- Predictions parquet contains y_true and proba columns.

Failure modes
-------------
- Missing columns or empty predictions file.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from stress_prediction.utils.config import project_paths
from stress_prediction.utils.metrics import compute_metrics_from_predictions


def task_evaluate_model(
    depends_on: Path = project_paths().predictions_parquet,
    produces: Path = project_paths().metrics_csv,
) -> None:
    """Compute metrics table and write it to CSV.

    Parameters
    ----------
    depends_on:
        Predictions parquet.
    produces:
        Metrics CSV path.
    """
    pred = pd.read_parquet(depends_on)

    metrics = compute_metrics_from_predictions(pred, y_col="y_true", proba_col="proba")

    produces.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(produces, index=False)