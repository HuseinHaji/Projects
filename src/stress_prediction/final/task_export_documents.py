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
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType

import pandas as pd

from stress_prediction.utils.config import project_paths

PATHS = project_paths()
ROOT = PATHS.root

FIGURE_DEPENDS_ON: Mapping[str, Path] = MappingProxyType(
    {
        "roc_curve": PATHS.fig_roc_curve,
        "predicted_probability": PATHS.fig_predicted_probability,
        "model_comparison_auc": PATHS.fig_model_comparison_auc,
        "volatility_stress": PATHS.fig_volatility_stress,
    }
)

FIGURE_PRODUCES: Mapping[str, Path] = MappingProxyType(
    {
        "roc_curve": ROOT / "documents" / "public" / "roc_curve.png",
        "predicted_probability": (
            ROOT / "documents" / "public" / "predicted_probability.png"
        ),
        "model_comparison_auc": (
            ROOT / "documents" / "public" / "model_comparison_auc.png"
        ),
        "volatility_stress": (ROOT / "documents" / "public" / "volatility_stress.png"),
    }
)

TABLE_DEPENDS_ON: Mapping[str, Path] = MappingProxyType(
    {
        "metrics": PATHS.tables_dir / "metrics.csv",
        "model_comparison": PATHS.tables_dir / "model_comparison.csv",
    }
)

TABLE_PRODUCES: Mapping[str, Path] = MappingProxyType(
    {
        "metrics": ROOT / "documents" / "tables" / "metrics.md",
        "model_comparison": ROOT / "documents" / "tables" / "model_comparison.md",
    }
)


def _write_markdown_table(source: Path, destination: Path) -> None:
    """Read a CSV file and write it as a Markdown table."""
    df = pd.read_csv(source)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        df.round(3).to_markdown(index=False) + "\n",
        encoding="utf-8",
    )


def task_export_document_figures(
    depends_on: Mapping[str, Path] = FIGURE_DEPENDS_ON,
    produces: Mapping[str, Path] = FIGURE_PRODUCES,
) -> None:
    """Copy final figures from ``bld/figures`` to ``documents/public``.

    Parameters
    ----------
    depends_on
        Source figures in ``bld/figures``.
    produces
        Destination figures in ``documents/public``.
    """
    for key, src in depends_on.items():
        dst = produces[key]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def task_export_document_tables(
    depends_on: Mapping[str, Path] = TABLE_DEPENDS_ON,
    produces: Mapping[str, Path] = TABLE_PRODUCES,
) -> None:
    """Convert CSV tables from ``bld/tables`` to Markdown tables.

    Parameters
    ----------
    depends_on
        Source CSV tables in ``bld/tables``.
    produces
        Destination Markdown tables in ``documents/tables``.
    """
    for key, src in depends_on.items():
        _write_markdown_table(source=src, destination=produces[key])
