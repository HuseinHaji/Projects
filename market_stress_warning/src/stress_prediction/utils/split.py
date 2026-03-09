"""Deterministic time-based splitting.

Purpose
-------
Create a train/test split based on time ordering, without any random shuffling.

Inputs
------
- DataFrame with a date column.

Outputs
-------
- DataFrame copy with a split column ('train'/'test').

Assumptions
-----------
- Input is already sorted by date, or at least has a usable date column.
- test_size is a fraction in (0, 1).

Failure modes
-------------
- ValueError if too few rows for the requested minimum train size.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TimeSplitResult:
    """Container for split output and cutoff date."""

    df: pd.DataFrame
    cutoff_date: pd.Timestamp


def add_time_split(
    df: pd.DataFrame,
    *,
    date_col: str = "date",
    split_col: str = "split",
    test_size: float = 0.2,
    min_train_size: int = 252,
) -> TimeSplitResult:
    """Add a deterministic time split column.

    Inputs
    ------
    df: DataFrame with a date column.
    date_col: Name of the date column.
    split_col: Output split column name.
    test_size: Fraction of rows assigned to the test split at the end of the sample.
    min_train_size: Minimum number of training rows required.

    Outputs
    -------
    TimeSplitResult with df and cutoff_date.

    Failure modes
    -------------
    - ValueError if test_size not in (0, 1), if date_col missing,
      or if min_train_size cannot be satisfied.
    """
    if not (0.0 < test_size < 1.0):
        raise ValueError("test_size must be in (0, 1)")
    if date_col not in df.columns:
        raise ValueError(f"Missing date column: {date_col}")

    tmp = df.sort_values(date_col, ascending=True).reset_index(drop=True).copy()
    n = tmp.shape[0]
    n_test = max(1, int(round(n * test_size)))
    n_train = n - n_test

    if n_train < min_train_size:
        raise ValueError(f"Not enough training rows: n_train={n_train}, min_train_size={min_train_size}")

    cutoff_date = tmp.loc[n_train - 1, date_col]
    tmp[split_col] = "train"
    tmp.loc[n_train:, split_col] = "test"

    return TimeSplitResult(df=tmp, cutoff_date=pd.Timestamp(cutoff_date))