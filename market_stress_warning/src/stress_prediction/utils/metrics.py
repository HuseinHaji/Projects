"""Model evaluation metrics."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    roc_auc_score,
)

from stress_prediction.utils.model import select_model_features


def compute_metrics_table(
    df: pd.DataFrame,
    model,
    *,
    split_col: str,
    label_col: str,
) -> pd.DataFrame:
    """Compute evaluation metrics for the test dataset.

    Purpose
    -------
    Evaluate the trained classification model on the test split using
    probabilistic predictions and standard binary classification metrics.

    Inputs
    ------
    df : pandas.DataFrame
        Dataset containing features, split indicators, and the true label.

    model : sklearn-compatible estimator
        Fitted model that implements `predict_proba`.

    split_col : str
        Column identifying dataset partitions (e.g., "train", "test").

    label_col : str
        Column containing the true binary label.

    Outputs
    -------
    pandas.DataFrame
        Single-row table containing evaluation metrics:
        - roc_auc : ROC AUC score
        - pr_auc : Precision–Recall AUC
        - brier_score : Brier probability calibration score
        - tn, fp, fn, tp : confusion matrix components

    Assumptions
    -----------
    - `split_col` contains a "test" partition.
    - `label_col` is binary (0/1) and may be stored as float.
    - The model implements `predict_proba`.

    Failure modes
    -------------
    ValueError
        Raised if no test observations are available.
    """
    test_df = df.loc[df[split_col] == "test"].copy()
    if test_df.empty:
        raise ValueError("No test observations found.")

    feature_cols = select_model_features(test_df)
    X_test = test_df[feature_cols]
    y_test = test_df[label_col].astype(int)

    proba = model.predict_proba(X_test)[:, 1]
    preds = (proba >= 0.5).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

    metrics = {
        "roc_auc": roc_auc_score(y_test, proba),
        "pr_auc": average_precision_score(y_test, proba),
        "brier_score": brier_score_loss(y_test, proba),
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }
    return pd.DataFrame([metrics])

def compute_metrics_from_predictions(
    pred: pd.DataFrame,
    *,
    y_col: str = "y_true",
    proba_col: str = "proba",
) -> pd.DataFrame:
    """Compute evaluation metrics from prediction outputs.

    Purpose
    -------
    Calculate summary performance metrics from a dataset containing
    true labels and predicted probabilities.

    Inputs
    ------
    pred : pandas.DataFrame
        DataFrame containing prediction results.

    y_col : str, default "y_true"
        Column containing the true binary labels.

    proba_col : str, default "proba"
        Column containing predicted probabilities for the positive class.

    Outputs
    -------
    pandas.DataFrame
        Single-row table with summary metrics:
        - auc : ROC AUC score
        - avg_precision : Precision–Recall AUC
        - n : number of observations
        - pos_rate : share of positive labels

    Assumptions
    -----------
    - `y_col` contains binary values (0/1).
    - `proba_col` contains predicted probabilities between 0 and 1.

    Failure modes
    -------------
    ValueError
        Raised if metric computation fails due to invalid inputs
        (e.g., only one class present).
    """
    y = pred[y_col].astype(int).to_numpy()
    p = pred[proba_col].astype(float).to_numpy()

    out = {
        "auc": [roc_auc_score(y, p)],
        "avg_precision": [average_precision_score(y, p)],
        "n": [int(len(pred))],
        "pos_rate": [float(y.mean())],
    }
    return pd.DataFrame(out)