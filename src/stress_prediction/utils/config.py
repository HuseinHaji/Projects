"""Central configuration for the stress_prediction project.

Purpose
-------
Define stable, importable configuration objects for:
- paths under the repository and bld/
- dataset schema choices
- feature engineering parameters
- model parameters

Inputs
------
None (module constants and small dataclasses).

Outputs
-------
Config dataclasses and constants used across tasks and package modules.

Assumptions
-----------
- Repository root is the current working directory when running `pixi run pytask`.
- Outputs must be written under `bld/`.

Failure modes
-------------
- If the working directory is not the repo root, path resolution may point to
  incorrect locations.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    """Project paths under the repository root.

    Inputs
    ------
    root: Repository root directory.

    Outputs
    -------
    Various derived paths used by tasks.

    Assumptions
    -----------
    - bld/ is the build output directory.
    """

    root: Path

    @property
    def bld(self) -> Path:
        return self.root / "bld"

    @property
    def data_raw_dir(self) -> Path:
        return self.bld / "data" / "raw"

    @property
    def data_clean_dir(self) -> Path:
        return self.bld / "data" / "clean"

    @property
    def data_features_dir(self) -> Path:
        return self.bld / "data" / "features"

    @property
    def models_dir(self) -> Path:
        return self.bld / "models"

    @property
    def tables_dir(self) -> Path:
        return self.bld / "tables"

    @property
    def figures_dir(self) -> Path:
        return self.bld / "figures"

    @property
    def raw_csv(self) -> Path:
        return self.data_raw_dir / "spx.csv"

    @property
    def raw_metadata(self) -> Path:
        return self.data_raw_dir / "spx_metadata.json"

    @property
    def clean_parquet(self) -> Path:
        return self.data_clean_dir / "spx_clean.parquet"

    @property
    def features_parquet(self) -> Path:
        return self.data_features_dir / "spx_features.parquet"
    
    @property
    def predictions_parquet(self) -> Path:
        return self.bld / "data" / "predictions" / "predictions.parquet"

    @property
    def threshold_json(self) -> Path:
        return self.data_features_dir / "threshold.json"

    @property
    def model_joblib(self) -> Path:
        return self.models_dir / "logreg.joblib"

    @property
    def metrics_csv(self) -> Path:
        return self.tables_dir / "metrics.csv"

    @property
    def fig_volatility_stress(self) -> Path:
        return self.figures_dir / "volatility_stress.png"

    @property
    def fig_roc_curve(self) -> Path:
        return self.figures_dir / "roc_curve.png"

    @property
    def fig_predicted_probability(self) -> Path:
        return self.figures_dir / "predicted_probability.png"
    
    @property
    def fig_model_comparison_auc(self) -> Path:
        return self.figures_dir / "model_comparison_auc.png"


@dataclass(frozen=True)
class DataConfig:
    """Data-related configuration."""

    stooq_url: str
    date_col_raw: str = "Date"
    close_col_raw: str = "Close"


@dataclass(frozen=True)
class FeatureConfig:
    """Feature engineering configuration."""

    return_col: str = "return"
    vol_col: str = "volatility"
    rolling_window_days: int = 21
    lag_days: int = 5
    test_size: float = 0.2
    min_train_size: int = 252
    threshold_quantile: float = 0.9
    label_col: str = "stress"
    split_col: str = "split"


@dataclass(frozen=True)
class ModelConfig:
    """Logistic regression configuration."""

    random_state: int = 0
    max_iter: int = 1000
    solver: str = "lbfgs"
    penalty: str = "l2"


def project_paths() -> Paths:
    """Create project paths based on the current working directory.

    Inputs
    ------
    None.

    Outputs
    -------
    Paths object rooted at Path.cwd().

    Failure modes
    -------------
    - If the working directory is not the repo root, derived paths will be wrong.
    """
    return Paths(root=Path.cwd())


DATA = DataConfig(stooq_url="https://stooq.com/q/d/l/?s=^spx&i=d")
FEATURES = FeatureConfig()
MODEL = ModelConfig()