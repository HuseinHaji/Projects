from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from stress_prediction.utils.clean import clean_spx_csv

EXPECTED_ROW_COUNT = 3


def test_clean_spx_outputs_expected_columns_and_sorted(tmp_path: Path) -> None:
    df = pd.DataFrame(
        {
            "Date": ["2020-01-03", "2020-01-02", "2020-01-01"],
            "Close": ["10.0", "9.0", "8.0"],
            "Open": [0, 0, 0],
        }
    )
    csv_path = tmp_path / "raw.csv"
    df.to_csv(csv_path, index=False)

    cleaned = clean_spx_csv(csv_path)
    out = cleaned.df

    assert list(out.columns) == ["date", "close"]
    assert out["date"].is_monotonic_increasing
    assert out["date"].dtype.kind in {"M"}
    assert out["close"].dtype.kind in {"f", "i"}
    assert out.shape[0] == EXPECTED_ROW_COUNT


def test_clean_spx_raises_on_duplicate_dates(tmp_path: Path) -> None:
    df = pd.DataFrame({"Date": ["2020-01-01", "2020-01-01"], "Close": [1.0, 2.0]})
    csv_path = tmp_path / "raw.csv"
    df.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="duplicate"):
        clean_spx_csv(csv_path)
