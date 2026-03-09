"""Export final document assets from build outputs.

Purpose
-------
Copy publication-ready figures from ``bld/figures`` to ``documents/public``
and convert selected CSV result tables from ``bld/tables`` to Markdown tables
in ``documents/tables`` for inclusion in the paper and presentation.

Inputs
------
- bld/figures/roc_curve.png
- bld/figures/predicted_probability.png
- bld/figures/model_comparison_auc.png
- bld/figures/volatility_stress.png
- bld/tables/metrics.csv
- bld/tables/model_comparison.csv

Outputs
-------
- documents/public/roc_curve.png
- documents/public/predicted_probability.png
- documents/public/model_comparison_auc.png
- documents/public/volatility_stress.png
- documents/tables/metrics.md
- documents/tables/model_comparison.md

Assumptions
-----------
- The required figures and CSV tables have already been created in ``bld``.
- CSV files are readable by pandas and suitable for Markdown export.

Failure modes
-------------
- Missing source files in ``bld``.
- Unreadable or malformed CSV tables.
- Missing write permissions for ``documents`` outputs.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from stress_prediction.utils.config import project_paths

PATHS = project_paths()
ROOT = PATHS.root


def _write_markdown_table(source: Path, destination: Path) -> None:
    """Read a CSV file and write it as a Markdown table."""
    df = pd.read_csv(source)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        df.round(3).to_markdown(index=False) + "\n",
        encoding="utf-8",
    )


def task_export_roc_curve(
    depends_on: Path = PATHS.fig_roc_curve,
    produces: Path = ROOT / "documents" / "public" / "roc_curve.png",
) -> None:
    """Copy the ROC curve figure to the documents directory."""
    produces.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(depends_on, produces)


def task_export_predicted_probability(
    depends_on: Path = PATHS.fig_predicted_probability,
    produces: Path = ROOT / "documents" / "public" / "predicted_probability.png",
) -> None:
    """Copy the predicted probability figure to the documents directory."""
    produces.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(depends_on, produces)


def task_export_model_comparison_auc(
    depends_on: Path = PATHS.fig_model_comparison_auc,
    produces: Path = ROOT / "documents" / "public" / "model_comparison_auc.png",
) -> None:
    """Copy the model comparison AUC figure to the documents directory."""
    produces.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(depends_on, produces)


def task_export_volatility_stress(
    depends_on: Path = PATHS.fig_volatility_stress,
    produces: Path = ROOT / "documents" / "public" / "volatility_stress.png",
) -> None:
    """Copy the volatility stress figure to the documents directory."""
    produces.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(depends_on, produces)


def task_export_metrics_table(
    depends_on: Path = PATHS.tables_dir / "metrics.csv",
    produces: Path = ROOT / "documents" / "tables" / "metrics.md",
) -> None:
    """Convert the metrics CSV table to a Markdown table."""
    _write_markdown_table(source=depends_on, destination=produces)


def task_export_model_comparison_table(
    depends_on: Path = PATHS.tables_dir / "model_comparison.csv",
    produces: Path = ROOT / "documents" / "tables" / "model_comparison.md",
) -> None:
    """Convert the model comparison CSV table to a Markdown table."""
    _write_markdown_table(source=depends_on, destination=produces)
