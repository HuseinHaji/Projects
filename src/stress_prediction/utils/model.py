"""Model training.

Purpose
-------
Train a logistic regression classifier for next-day stress.

Inputs
------
df : pandas.DataFrame with features, split, and label column
split_col : str
label_col : str

Outputs
-------
Fitted sklearn Pipeline (StandardScaler + LogisticRegression).

Assumptions
-----------
- split_col has 'train' and 'test'
- label_col is binary (0/1) and may be float due to shift; will be cast to int

Failure modes
-------------
- ValueError if no train data.
"""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def select_model_features(df: pd.DataFrame) -> list[str]:
    """Select feature columns used for model training.

    Purpose
    -------
    Identify valid predictor variables from the dataset while avoiding
    look-ahead bias. Contemporaneous volatility is excluded because it
    may contain information not available at prediction time.

    Inputs
    ------
    df : pandas.DataFrame
        DataFrame containing engineered feature columns.

    Outputs
    -------
    list[str]
        Ordered list of column names used as model features.

    Feature Selection Rules
    -----------------------
    Included
    - "return" (current daily return)
    - Columns starting with "return_lag"
    - Columns starting with "volatility_lag"

    Excluded
    - Contemporaneous volatility columns.

    Assumptions
    -----------
    - Feature engineering produced columns following the naming
      conventions "return_lag*" and "volatility_lag*".

    Failure modes
    -------------
    - If none of the expected columns exist, the returned list may be empty.
    """
    cols: list[str] = []
    if "return" in df.columns:
        cols.append("return")
    cols.extend(sorted([c for c in df.columns if c.startswith("return_lag")]))
    cols.extend(sorted([c for c in df.columns if c.startswith("volatility_lag")]))
    return cols


def train_logistic_regression(
    df: pd.DataFrame,
    *,
    split_col: str = "split",
    label_col: str = "stress",
    random_state: int = 0,
    max_iter: int = 1000,
    solver: str = "lbfgs",
) -> Pipeline:
    """Train a logistic regression model for next-day stress prediction.

    Purpose
    -------
    Fit a binary classification model that predicts whether the next
    trading day will be a stress period based on lagged return and
    volatility features.

    Inputs
    ------
    df : pandas.DataFrame
        Dataset containing feature columns, a split indicator, and
        the binary stress label.

    split_col : str, default "split"
        Column specifying dataset partitions. Only rows with value
        "train" are used for model training.

    label_col : str, default "stress"
        Binary target variable indicating next-day stress.

    random_state : int, default 0
        Random seed for reproducibility of the LogisticRegression model.

    max_iter : int, default 1000
        Maximum number of iterations allowed for the solver.

    solver : str, default "lbfgs"
        Optimization algorithm used by LogisticRegression.

    Outputs
    -------
    sklearn.pipeline.Pipeline
        A fitted pipeline consisting of:
        - StandardScaler
        - LogisticRegression classifier

    Assumptions
    -----------
    - `split_col` contains a "train" subset.
    - `label_col` represents a binary variable (0/1).
    - Feature columns follow the naming conventions used in
      `select_model_features`.

    Failure modes
    -------------
    ValueError
        Raised if the dataset contains no training observations.
    """
    train_df = df.loc[df[split_col] == "train"].copy()
    if train_df.empty:
        raise ValueError("No training observations found.")

    feature_cols = select_model_features(train_df)
    X_train = train_df[feature_cols]
    y_train = train_df[label_col].astype(int)

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("logreg", LogisticRegression(random_state=random_state, max_iter=max_iter, solver=solver)),
        ]
    )
    pipeline.fit(X_train, y_train)
    return pipeline