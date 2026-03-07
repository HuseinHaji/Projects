"""Download raw S&P 500 (^SPX) data from Stooq.

Purpose
-------
Fetch the latest daily S&P 500 index data from Stooq and store the raw CSV plus
download metadata under the build directory.

Inputs
------
None (downloads from a fixed URL defined in configuration).

Outputs
-------
- bld/data/raw/spx.csv
- bld/data/raw/spx_metadata.json

Assumptions
-----------
- Network access is available when running the task.
- Stooq provides a CSV with Date/Close columns as configured.

Failure modes
-------------
- Network errors or invalid responses from Stooq.
- File write permissions missing for bld/.
"""

from __future__ import annotations

from pathlib import Path

from stress_prediction.utils.config import DATA, project_paths
from stress_prediction.utils.download import download_stooq_csv, write_raw_and_metadata


def task_download_spx(
    produces: dict[str, Path] = {
        "csv": project_paths().raw_csv,
        "metadata": project_paths().raw_metadata,
    }
) -> None:
    """Download raw CSV and metadata and write them to bld/.

    Parameters
    ----------
    produces:
        Output paths for the raw CSV and metadata JSON.
    """
    csv_bytes, meta = download_stooq_csv(DATA.stooq_url)
    write_raw_and_metadata(
        csv_bytes,
        meta,
        csv_path=produces["csv"],
        metadata_path=produces["metadata"],
    )