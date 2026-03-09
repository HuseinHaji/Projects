from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_phase2_tables(
    tables: dict[str, pd.DataFrame],
    output_dir: str = "data/processed/phase2",
    save_parquet: bool = False,
) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for name, df in tables.items():
        csv_path = output_path / f"{name}.csv"
        df.to_csv(csv_path, index=False)
        print(f"[CSV] {name}: {df.shape} -> {csv_path}")

        if save_parquet:
            parquet_path = output_path / f"{name}.parquet"
            df.to_parquet(parquet_path, index=False)
            print(f"[PARQUET] {name}: {df.shape} -> {parquet_path}")