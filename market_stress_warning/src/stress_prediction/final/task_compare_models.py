"""Compare the main model to baselines on the expanding-window test set.

Purpose
-------
Create a compact baseline comparison table for:
1) State-feature logistic regression (main model output already computed).
2) Returns-only logistic regression (recomputed via expanding-window backtest).
3) Naive persistence score using a lagged volatility proxy (vol_21 percentile).

Inputs
------
- bld/data/features/spx_features.parquet
- bld/data/predictions/predictions.parquet

Outputs
-------
- bld/tables/model_comparison.csv

Assumptions
-----------
- 'split' defines the test period.
- The naive baseline uses vol_21, which is lagged in feature construction.

Failure modes
-------------
- Missing columns (e.g., vol_21) or empty train distribution.
- No overlap between test dates and prediction dates.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

from stress_prediction.utils.backtest import expanding_window_predict_proba
from stress_prediction.utils.config import FEATURES, MODEL, project_paths


def _summarize(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    """Summarize classification performance for a probability score."""
    y = y.astype(int)
    p = p.astype(float)
    return {
        "auc": float(roc_auc_score(y, p)),
        "avg_precision": float(average_precision_score(y, p)),
        "brier": float(brier_score_loss(y, p)),
        "pos_rate": float(y.mean()),
        "n": int(len(y)),
    }


def task_model_comparison(
    depends_on: dict[str, Path] = {
        "features": project_paths().features_parquet,
        "state_pred": project_paths().predictions_parquet,  
    },
    produces: Path = project_paths().tables_dir / "model_comparison.csv",
) -> None:
    """Compute baseline comparison metrics and write a CSV summary table."""
    df = pd.read_parquet(depends_on["features"]).sort_values("date").reset_index(drop=True)
    state_pred = pd.read_parquet(depends_on["state_pred"]).sort_values("date").reset_index(drop=True)

    df["date"] = pd.to_datetime(df["date"])
    state_pred["date"] = pd.to_datetime(state_pred["date"])


    test = df[df[FEATURES.split_col].eq("test")].copy()

    state_pred = state_pred.rename(columns={"proba": "proba_state"})
    test = test.merge(
        state_pred[["date", "y_true", "proba_state"]],
        on="date",
        how="inner",
        validate="one_to_one",
    )

    y_true = test["y_true"].astype(int).to_numpy()
    p_state = test["proba_state"].astype(float).to_numpy()

    returns_cols = [
        c
        for c in df.columns
        if c == FEATURES.return_col or c.startswith(f"{FEATURES.return_col}_lag")
    ]
    base_model = LogisticRegression(
        random_state=MODEL.random_state,
        max_iter=MODEL.max_iter,
        solver=MODEL.solver,
    )
    ret_res = expanding_window_predict_proba(
        df,
        model=base_model,
        date_col="date",
        feature_cols=returns_cols,
        label_col=FEATURES.label_col,
        split_col=FEATURES.split_col,
        refit_freq="MS",
    )
    ret_pred = ret_res.df_pred.copy()
    ret_pred["date"] = pd.to_datetime(ret_pred["date"])
    ret_pred = ret_pred.rename(columns={"proba": "proba_returns"})

    test = test.merge(ret_pred[["date", "proba_returns"]], on="date", how="left", validate="one_to_one")
    p_returns = test["proba_returns"].astype(float).to_numpy()

    if "vol_21" not in df.columns:
        raise ValueError("vol_21 is missing; needed for naive baseline score.")

    train_vals = df.loc[df[FEATURES.split_col].eq("train"), "vol_21"].dropna().to_numpy()
    if train_vals.size == 0:
        raise ValueError("vol_21 train distribution is empty; cannot compute naive baseline.")

    x = test["vol_21"].to_numpy()
    p_naive = np.searchsorted(np.sort(train_vals), x, side="right") / float(train_vals.size)

    rows = []
    rows.append({"model": "state_logreg", **_summarize(y_true, p_state)})
    rows.append({"model": "returns_only_logreg", **_summarize(y_true, p_returns)})
    rows.append({"model": "naive_vol21_percentile", **_summarize(y_true, p_naive)})

    out = pd.DataFrame(rows)

    produces.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(produces, index=False)