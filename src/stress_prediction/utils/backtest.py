from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd
from sklearn.base import clone


@dataclass(frozen=True)
class BacktestResult:
    """Store outputs from the expanding-window backtest.

    Attributes
    ----------
    df_pred : pandas.DataFrame
        DataFrame containing prediction results for the test period,
        including dates, true labels, predicted probabilities, and split labels.

    metadata : dict[str, Any]
        Dictionary with summary information about the backtest, such as
        refit frequency, number of predictions, and test-period boundaries.
    """
    df_pred: pd.DataFrame
    metadata: dict[str, Any]


def expanding_window_predict_proba(
    df: pd.DataFrame,
    *,
    model,
    date_col: str,
    feature_cols: list[str],
    label_col: str,
    split_col: str,
    refit_freq: str = "MS",  
) -> BacktestResult:
    """Run an expanding-window backtest with periodic model refitting.

    Purpose
    -------
    Simulate a realistic forecasting workflow by repeatedly refitting the
    model on all data available up to each refit date and then generating
    predicted probabilities for the subsequent test block.

    Inputs
    ------
    df : pandas.DataFrame
        Dataset containing dates, features, labels, and split assignments.

    model : sklearn-compatible estimator
        Unfitted or base model object that supports `fit` and `predict_proba`.
        A fresh clone is fit at each refit date.

    date_col : str
        Column containing observation dates.

    feature_cols : list[str]
        List of feature column names used for model training and prediction.

    label_col : str
        Column containing the binary target variable.

    split_col : str
        Column identifying dataset partitions. Rows with value "test" define
        the forecast period over which predictions are generated.

    refit_freq : str, default "MS"
        Pandas date offset string controlling how often the model is refit.
        "MS" means month start.

    Outputs
    -------
    BacktestResult
        Dataclass containing:
        - df_pred: prediction table with dates, true labels, probabilities,
          and split labels
        - metadata: summary information about the backtest configuration
          and output coverage

    Method
    ------
    - Sort data by date.
    - Identify the test period from rows where `split_col == "test"`.
    - Create refit dates using `refit_freq`.
    - For each refit date:
      - train on all rows with date earlier than the refit date
      - predict probabilities for test rows between the current and next refit date
    - Concatenate all prediction blocks into one ordered output table.

    Assumptions
    -----------
    - `date_col` can be converted to pandas datetime.
    - `label_col` is binary and can be cast to integer.
    - `feature_cols` exist in `df`.
    - `model` supports `fit`, `predict_proba`, and sklearn cloning.
    - Test rows are identified by `split_col == "test"`.

    Failure modes
    -------------
    ValueError
        Raised if no test rows are found.

    ValueError
        Raised if no predictions are produced, for example because no
        training data exists before refit dates or test blocks are empty.
    """
    df = df.sort_values(date_col).reset_index(drop=True).copy()
    df[date_col] = pd.to_datetime(df[date_col])

    test_mask = df[split_col].eq("test")
    test_dates = df.loc[test_mask, date_col]

    if test_dates.empty:
        raise ValueError("No test rows found. Check split_col values.")

    start = test_dates.min()
    end = test_dates.max()

    refit_dates = pd.date_range(start=start, end=end, freq=refit_freq)
    if len(refit_dates) == 0:
        refit_dates = pd.DatetimeIndex([start])

    preds: list[pd.DataFrame] = []

    for i, refit_date in enumerate(refit_dates):
        next_refit = refit_dates[i + 1] if i + 1 < len(refit_dates) else (end + pd.Timedelta(days=1))

        train = df[df[date_col] < refit_date]
        test_block = df[(df[date_col] >= refit_date) & (df[date_col] < next_refit) & test_mask]

        if train.empty or test_block.empty:
            continue

        X_train = train[feature_cols]
        y_train = train[label_col].astype(int)

        X_test = test_block[feature_cols]

        m = clone(model)
        m.fit(X_train, y_train)

        proba = m.predict_proba(X_test)[:, 1]

        out = pd.DataFrame(
            {
                date_col: test_block[date_col].values,
                "y_true": test_block[label_col].astype(int).values,
                "proba": proba,
                split_col: test_block[split_col].values,
            }
        )
        preds.append(out)

    if not preds:
        raise ValueError("Backtest produced no predictions (likely no train/test overlap by refit blocks).")

    df_pred = pd.concat(preds, ignore_index=True).sort_values(date_col).reset_index(drop=True)

    meta: dict[str, Any] = {
        "refit_freq": refit_freq,
        "n_pred": int(len(df_pred)),
        "start_test": str(start.date()),
        "end_test": str(end.date()),
    }
    return BacktestResult(df_pred=df_pred, metadata=meta)