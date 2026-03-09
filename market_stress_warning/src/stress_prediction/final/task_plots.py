"""Create standard evaluation plots from backtest predictions.

Purpose
-------
Generate the ROC curve and the predicted probability time series for the
expanding-window test predictions.

Inputs
------
- bld/data/predictions/predictions.parquet

Outputs
-------
- bld/figures/roc_curve.png
- bld/figures/predicted_probability.png

Assumptions
-----------
- Predictions parquet contains date, y_true, and proba.

Failure modes
-------------
- Missing columns or unreadable predictions parquet.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from stress_prediction.utils.config import project_paths
from stress_prediction.utils.plots import (
    plot_predicted_probability_from_predictions,
    plot_roc_curve_from_predictions,
)


def task_plots(
    depends_on: Path = project_paths().predictions_parquet,
    produces: dict[str, Path] = {
        "roc": project_paths().fig_roc_curve,
        "proba": project_paths().fig_predicted_probability,
    },
) -> None:
    """Create ROC curve and probability time-series plots.

    Parameters
    ----------
    depends_on:
        Predictions parquet.
    produces:
        Output figure paths for ROC and probability plots.
    """
    pred = pd.read_parquet(depends_on)

    plot_roc_curve_from_predictions(
        pred=pred,
        y_col="y_true",
        proba_col="proba",
        out_path=produces["roc"],
    )

    plot_predicted_probability_from_predictions(
        pred=pred,
        date_col="date",
        proba_col="proba",
        out_path=produces["proba"],
    )