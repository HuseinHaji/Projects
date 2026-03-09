"""Cleaning and validation of raw S&P 500 data.

Purpose
-------
Transform the raw Stooq CSV to a minimal, validated dataset:
- parse dates
- select close price
- validate sorting, duplicates, and missing values
- output a clean DataFrame suitable for feature engineering

Inputs
------
- Raw CSV path.

Outputs
-------
- pandas DataFrame with columns: date, close.

Assumptions
-----------
- Raw CSV contains Date and Close columns.
- Date is parseable as YYYY-MM-DD.

Failure modes
-------------
- ValueError with clear messages if schema/ordering assumptions are violated.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class CleanedSpx:
    """Container for a cleaned dataset."""

    df: pd.DataFrame


def _require_columns(columns: list[str], required: list[str]) -> None:
    missing = [c for c in required if c not in columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def clean_spx_csv(csv_path: Path, *, date_col: str = "Date", close_col: str = "Close") -> CleanedSpx:
    """Clean Stooq SPX CSV into a validated two-column frame.

    Inputs
    ------
    csv_path: Path to raw CSV.
    date_col: Name of the date column in the raw file.
    close_col: Name of the close price column in the raw file.

    Outputs
    -------
    CleanedSpx with df columns: date (datetime64[ns]), close (float).

    Assumptions
    -----------
    - date_col and close_col exist in the CSV.

    Failure modes
    -------------
    - ValueError if required columns are missing, dates cannot be parsed,
      duplicates exist, or close contains missing values.
    """
    raw = pd.read_csv(csv_path)
    _require_columns(list(raw.columns), [date_col, close_col])

    df = raw[[date_col, close_col]].copy()
    df = df.rename(columns={date_col: "date", close_col: "close"})

    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=False)
    bad_dates = int(df["date"].isna().sum())
    if bad_dates:
        raise ValueError(f"Found {bad_dates} unparseable dates in raw data")

    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    bad_close = int(df["close"].isna().sum())
    if bad_close:
        raise ValueError(f"Found {bad_close} missing/non-numeric close values in raw data")

    df = df.sort_values("date", ascending=True).reset_index(drop=True)
    if df["date"].duplicated().any():
        raise ValueError("Found duplicate dates after sorting")

    if not df["date"].is_monotonic_increasing:
        raise ValueError("Dates are not monotonic increasing after sorting")

    return CleanedSpx(df=df)