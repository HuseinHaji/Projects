"""Download raw S&P 500 daily data from Stooq with metadata.

Purpose
-------
Fetch the CSV from Stooq, write it to disk, and store metadata including a sha256
digest so results are auditable and reproducible.

Inputs
------
url: CSV URL.
timeout_seconds: HTTP timeout.

Outputs
-------
- CSV bytes written to a target path.
- JSON metadata written to a target path.

Assumptions
-----------
- Stooq returns a CSV body.
- Network access is available.

Failure modes
-------------
- requests exceptions on network errors.
- Non-200 HTTP response.
- Empty response body.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import requests

from stress_prediction.utils.utils import atomic_write_bytes, sha256_bytes, write_json


def download_stooq_csv(url: str, *, timeout_seconds: int = 30) -> tuple[bytes, dict[str, object]]:
    """Download CSV bytes and create metadata.

    Inputs
    ------
    url: Stooq CSV URL.
    timeout_seconds: Timeout for the GET request.

    Outputs
    -------
    (csv_bytes, metadata_dict)

    Failure modes
    -------------
    - RuntimeError if HTTP status is not 200 or response is empty.
    """
    resp = requests.get(url, timeout=timeout_seconds)
    if resp.status_code != 200:
        raise RuntimeError(f"Download failed with status_code={resp.status_code}")
    data = resp.content
    if not data:
        raise RuntimeError("Download returned an empty response body")

    digest = sha256_bytes(data)
    now = datetime.now(timezone.utc).isoformat()

    meta: dict[str, object] = {
        "source": "stooq",
        "url": url,
        "fetched_at_utc": now,
        "sha256": digest,
        "n_bytes": len(data),
        "content_type": resp.headers.get("Content-Type"),
    }
    return data, meta


def write_raw_and_metadata(csv_bytes: bytes, metadata: dict[str, object], *, csv_path: Path, metadata_path: Path) -> None:
    """Write raw CSV bytes and metadata to disk.

    Inputs
    ------
    csv_bytes: Raw CSV bytes.
    metadata: Metadata dictionary.
    csv_path: Output path for the raw CSV.
    metadata_path: Output path for the JSON metadata.

    Outputs
    -------
    None.
    """
    atomic_write_bytes(csv_path, csv_bytes)
    write_json(metadata_path, metadata)