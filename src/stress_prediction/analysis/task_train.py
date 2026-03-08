"""Train a logistic regression model on the training split.

Purpose
-------
Fit the logistic regression classifier using the features dataset and save the
trained model artifact for reuse or inspection.

Inputs
------
- bld/data/features/spx_features.parquet

Outputs
-------
- bld/models/logreg.joblib

Assumptions
-----------
- The dataset contains a 'split' column with 'train' rows.
- The model trainer selects its own feature columns internally.

Failure modes
-------------
- Missing feature columns or label column.
- Empty training set.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from stress_prediction.utils.config import MODEL, project_paths
from stress_prediction.utils.model import train_logistic_regression

PATHS = project_paths()


def task_train_model(
    depends_on: Path = PATHS.features_parquet,
    produces: Path = PATHS.model_joblib,
) -> None:
    """Train logistic regression on TRAIN data and save the fitted model.

    Parameters
    ----------
    depends_on:
        Features parquet file.
    produces:
        Model artifact path (joblib).
    """
    df = pd.read_parquet(depends_on)
    model = train_logistic_regression(
        df,
        split_col="split",
        label_col="stress",
        random_state=MODEL.random_state,
        max_iter=MODEL.max_iter,
        solver=MODEL.solver,
    )
    produces.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, produces)
