"""Plot baseline model comparison results.

Purpose
-------
Create a simple AUC bar chart from the model comparison table.

Inputs
------
- bld/tables/model_comparison.csv

Outputs
-------
- bld/figures/model_comparison_auc.png

Assumptions
-----------
- model_comparison.csv contains columns: model, auc.

Failure modes
-------------
- Missing CSV or missing required columns.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from stress_prediction.utils.config import project_paths


def task_plot_model_comparison_auc(
    depends_on: Path = project_paths().tables_dir / "model_comparison.csv",
    produces: Path = project_paths().fig_model_comparison_auc,
) -> None:
    """Read model comparison CSV and write an AUC comparison plot."""
    df = pd.read_csv(depends_on)

    order = ["state_logreg", "naive_vol21_percentile", "returns_only_logreg"]
    df["model"] = pd.Categorical(df["model"], categories=order, ordered=True)
    df = df.sort_values("model")

    plt.figure()
    plt.bar(df["model"].astype(str), df["auc"])
    plt.ylim(0, 1)
    plt.xlabel("Model")
    plt.ylabel("AUC (Test, expanding window)")
    plt.title("Model Comparison (AUC)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    produces.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(produces)
    plt.close()