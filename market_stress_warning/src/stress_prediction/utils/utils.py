"""Small, reusable utilities for IO and hashing.

Purpose
-------
Provide tiny helpers used across the pipeline:
- ensure directories exist
- write/read JSON
- compute sha256
- atomic file writes for robustness

Inputs
------
Paths, bytes, JSON-serializable dicts.

Outputs
-------
Files written to disk and helper return values.

Assumptions
-----------
- Callers pass correct paths and JSON-serializable objects.

Failure modes
-------------
- Permission errors on write.
- JSON encoding errors for non-serializable objects.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def ensure_dir(path: Path) -> None:
    """Create a directory if it does not exist.

    Inputs
    ------
    path: Directory path.

    Outputs
    -------
    None.

    Failure modes
    -------------
    - OSError if directory cannot be created.
    """
    path.mkdir(parents=True, exist_ok=True)


def sha256_bytes(data: bytes) -> str:
    """Compute sha256 digest of bytes.

    Inputs
    ------
    data: Raw bytes.

    Outputs
    -------
    Hex digest string.
    """
    return hashlib.sha256(data).hexdigest()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """Atomically write bytes to a file.

    Inputs
    ------
    path: Output path.
    data: Bytes to write.

    Outputs
    -------
    None.

    Assumptions
    -----------
    - Path parent exists or can be created by caller.

    Failure modes
    -------------
    - OSError if writing fails.
    """
    dir_path = path.parent
    ensure_dir(dir_path)
    fd, tmp = tempfile.mkstemp(dir=dir_path, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def write_json(path: Path, obj: dict[str, Any]) -> None:
    """Write a JSON file with deterministic formatting.

    Inputs
    ------
    path: Output path.
    obj: JSON-serializable dictionary.

    Outputs
    -------
    None.

    Failure modes
    -------------
    - TypeError if obj is not JSON-serializable.
    - OSError if writing fails.
    """
    text = json.dumps(obj, indent=2, sort_keys=True) + "\n"
    atomic_write_bytes(path, text.encode("utf-8"))


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file.

    Inputs
    ------
    path: Path to JSON file.

    Outputs
    -------
    Parsed dictionary.

    Failure modes
    -------------
    - FileNotFoundError if missing.
    - JSONDecodeError if invalid JSON.
    """
    return json.loads(path.read_text(encoding="utf-8"))