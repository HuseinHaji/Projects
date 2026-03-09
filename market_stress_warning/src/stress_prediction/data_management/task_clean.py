"""Clean raw S&P 500 (^SPX) CSV into a validated parquet dataset.

Purpose
-------
Read the downloaded raw Stooq CSV, validate and standardize column names/types,
and write a clean parquet file used by downstream feature engineering.

Inputs
------
- bld/data/raw/spx.csv

Outputs
-------
- bld/data/clean/spx_clean.parquet

Assumptions
-----------
- The raw CSV uses the configured Date and Close column names.
- The pipeline uses a post-1990 sample for stability and speed.

Failure modes
-------------
- Raw file missing or malformed.
- Date parsing failures or non-numeric close prices.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from stress_prediction.utils.clean import clean_spx_csv
from stress_prediction.utils.config import DATA, project_paths


def task_clean_spx(
    depends_on: Path = project_paths().raw_csv,
    produces: Path = project_paths().clean_parquet,
) -> None:
    """Clean the raw CSV and write a clean parquet dataset.

    Parameters
    ----------
    depends_on:
        Path to the raw CSV.
    produces:
        Path to the cleaned parquet file.
    """
    cleaned = clean_spx_csv(
        depends_on,
        date_col=DATA.date_col_raw,
        close_col=DATA.close_col_raw,
    )

    df = cleaned.df
    df = df[df["date"] >= "1990-01-01"].reset_index(drop=True)

    produces.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(produces, index=False)