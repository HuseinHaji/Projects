"""Plotting utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import auc

from stress_prediction.utils.model import select_model_features
from sklearn.metrics import roc_curve, roc_auc_score


def plot_roc_curve(
    *,
    df: pd.DataFrame,
    model,
    split_col: str,
    label_col: str,
    out_path: Path,
) -> None:
    """Plot ROC curve for the test dataset.

    Purpose
    -------
    Visualize the model's classification performance on the test split
    using the Receiver Operating Characteristic (ROC) curve.

    Inputs
    ------
    df : pandas.DataFrame
        Dataset containing features, split indicators, and labels.

    model : sklearn-compatible estimator
        Fitted model implementing `predict_proba`.

    split_col : str
        Column identifying dataset partitions.

    label_col : str
        Column containing the true binary label.

    out_path : pathlib.Path
        File path where the plot image will be saved.

    Outputs
    -------
    None
        Saves the ROC curve figure to disk.

    Assumptions
    -----------
    - `split_col` contains a "test" partition.
    - `label_col` is binary (0/1).
    - The model implements `predict_proba`.

    Failure modes
    -------------
    ValueError
        Raised if the test dataset is empty.
    """
    test_df = df.loc[df[split_col] == "test"].copy()
    if test_df.empty:
        raise ValueError("No test observations found for ROC plot.")

    X = test_df[select_model_features(test_df)]
    y = test_df[label_col].astype(int).to_numpy()
    proba = model.predict_proba(X)[:, 1]

    fpr, tpr, _ = roc_curve(y, proba)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", label="Random")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve (Test Set)")
    ax.legend(loc="lower right")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_predicted_probability(
    *,
    df: pd.DataFrame,
    model,
    split_col: str,
    out_path: Path,
) -> None:
    """Plot predicted stress probabilities for the test dataset.

    Purpose
    -------
    Visualize predicted probabilities of the stress regime across the
    test period.

    Inputs
    ------
    df : pandas.DataFrame
        Dataset containing features and split indicators.

    model : sklearn-compatible estimator
        Fitted model implementing `predict_proba`.

    split_col : str
        Column identifying dataset partitions.

    out_path : pathlib.Path
        File path where the plot image will be saved.

    Outputs
    -------
    None
        Saves the probability time-series plot to disk.

    Assumptions
    -----------
    - `split_col` contains a "test" partition.
    - A "date" column may optionally exist for the x-axis.

    Failure modes
    -------------
    ValueError
        Raised if the test dataset is empty.
    """
    test_df = df.loc[df[split_col] == "test"].copy()
    if test_df.empty:
        raise ValueError("No test observations found for probability plot.")

    X = test_df[select_model_features(test_df)]
    proba = model.predict_proba(X)[:, 1]

    if "date" in test_df.columns:
        x = pd.to_datetime(test_df["date"])
        x_label = "Date"
    else:
        x = np.arange(len(test_df))
        x_label = "Test Observation Index"

    fig, ax = plt.subplots()
    ax.plot(x, proba)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Predicted stress probability")
    ax.set_title("Predicted Stress Probability (Test Set)")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

def plot_volatility_stress(
    *,
    df: pd.DataFrame,
    split_col: str,
    label_col: str,
    vol_col: str,
    threshold: float,
    out_path: Path,
) -> None:
    """Plot volatility with highlighted stress periods.

    Purpose
    -------
    Visualize rolling market volatility and highlight observations
    classified as stress regimes relative to a volatility threshold.

    Inputs
    ------
    df : pandas.DataFrame
        Dataset containing volatility measures and stress labels.

    split_col : str
        Column identifying dataset partitions.

    label_col : str
        Column containing the binary stress indicator.

    vol_col : str
        Column containing the volatility measure.

    threshold : float
        Volatility level used to define stress regimes.

    out_path : pathlib.Path
        File path where the plot image will be saved.

    Outputs
    -------
    None
        Saves the volatility–stress plot to disk.

    Assumptions
    -----------
    - `label_col` contains binary stress indicators.
    - `vol_col` exists in the dataset.

    Failure modes
    -------------
    ValueError
        Raised if the test dataset is empty.
    """
    test_df = df.loc[df[split_col] == "test"].copy()
    if test_df.empty:
        raise ValueError("No test observations found for volatility-stress plot.")

    if "date" in test_df.columns:
        x = pd.to_datetime(test_df["date"])
        x_label = "Date"
    else:
        x = np.arange(len(test_df))
        x_label = "Test Observation Index"

    fig, ax = plt.subplots()
    ax.plot(x, test_df[vol_col], label="Rolling volatility")
    ax.axhline(threshold, linestyle="--", label="Stress threshold")

    mask = test_df[label_col].astype(int) == 1
    if bool(mask.any()):
        ax.scatter(x[mask], test_df.loc[mask, vol_col], label="Stress days")

    ax.set_xlabel(x_label)
    ax.set_ylabel("Volatility")
    ax.set_title("Volatility and Stress Regime (Test Set)")
    ax.legend(loc="upper left")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

def plot_roc_curve_from_predictions(
    *,
    pred: pd.DataFrame,
    y_col: str,
    proba_col: str,
    out_path: Path,
) -> None:
    """Plot ROC curve from prediction results.

    Purpose
    -------
    Generate a ROC curve using stored prediction outputs rather than
    directly using a trained model.

    Inputs
    ------
    pred : pandas.DataFrame
        DataFrame containing predicted probabilities and true labels.

    y_col : str
        Column containing the true binary labels.

    proba_col : str
        Column containing predicted probabilities for the positive class.

    out_path : pathlib.Path
        File path where the plot image will be saved.

    Outputs
    -------
    None
        Saves the ROC curve plot to disk.

    Assumptions
    -----------
    - `y_col` contains binary values (0/1).
    - `proba_col` contains valid probability values between 0 and 1.
    """
    y = pred[y_col].astype(int).to_numpy()
    p = pred[proba_col].astype(float).to_numpy()

    fpr, tpr, _ = roc_curve(y, p)
    auc = roc_auc_score(y, p)

    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--", label="Random")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve (Expanding Window Test)")
    plt.legend()
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    plt.close()


def plot_predicted_probability_from_predictions(
    *,
    pred: pd.DataFrame,
    date_col: str,
    proba_col: str,
    out_path: Path,
) -> None:
    """Plot predicted stress probability over time.

    Purpose
    -------
    Visualize predicted stress probabilities across time using stored
    prediction results from an expanding-window evaluation.

    Inputs
    ------
    pred : pandas.DataFrame
        DataFrame containing prediction outputs.

    date_col : str
        Column containing observation dates.

    proba_col : str
        Column containing predicted probabilities for the positive class.

    out_path : pathlib.Path
        File path where the plot image will be saved.

    Outputs
    -------
    None
        Saves the probability time-series plot to disk.

    Assumptions
    -----------
    - `date_col` contains valid date values.
    - `proba_col` contains probabilities between 0 and 1.
    """
    df = pred.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    plt.figure()
    plt.plot(df[date_col], df[proba_col])
    plt.xlabel("Date")
    plt.ylabel("Predicted stress probability")
    plt.title("Predicted Stress Probability (Expanding Window Test)")
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    plt.close()