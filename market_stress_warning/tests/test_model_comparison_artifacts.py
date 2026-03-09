from __future__ import annotations

import pandas as pd

from stress_prediction.utils.config import project_paths


def test_model_comparison_table_exists_and_has_metrics() -> None:
    paths = project_paths()
    cmp_path = paths.tables_dir / "model_comparison.csv"

    df = pd.read_csv(cmp_path)

    assert {"model", "auc", "avg_precision", "brier", "pos_rate", "n"} <= set(
        df.columns
    )
    models = set(df["model"].astype(str))
    assert {"state_logreg", "returns_only_logreg", "naive_vol21_percentile"} <= models
    assert df["auc"].between(0.0, 1.0).all()
    assert df["avg_precision"].between(0.0, 1.0).all()
    assert df["brier"].between(0.0, 1.0).all()
    assert df[["auc", "avg_precision", "brier", "pos_rate", "n"]].notna().all().all()
