"""Plot realized volatility and stress regime markers on the test set.

Purpose
-------
Create a diagnostic plot of rolling volatility over the test period together
with the stress threshold and stress-day markers.

Inputs
------
- bld/data/features/spx_features.parquet
- bld/data/features/threshold.json

Outputs
-------
- bld/figures/volatility_stress.png

Assumptions
-----------
- Features parquet contains the rolling volatility column.
- Threshold JSON contains a numeric "threshold" field.

Failure modes
-------------
- Missing volatility column.
- Malformed JSON metadata.
"""
from __future__ import annotations

from pathlib import Path
import json

import pandas as pd

from stress_prediction.utils.config import FEATURES, project_paths
from stress_prediction.utils.plots import plot_volatility_stress


def task_volatility_stress(
    depends_on: dict[str, Path] = {
        "features": project_paths().features_parquet,
        "threshold": project_paths().threshold_json,
    },
    produces: Path = project_paths().fig_volatility_stress,
) -> None:
    """Create volatility+threshold plot for the test split.

    Parameters
    ----------
    depends_on:
        Paths to the features parquet and threshold metadata JSON.
    produces:
        Output figure path.
    """
    df = pd.read_parquet(depends_on["features"])
    meta = json.loads(Path(depends_on["threshold"]).read_text())
    threshold = float(meta["threshold"])

    plot_volatility_stress(
        df=df,
        split_col=FEATURES.split_col,
        label_col=FEATURES.label_col,
        vol_col=FEATURES.vol_col,
        threshold=threshold,
        out_path=produces,
    )