from __future__ import annotations

from pathlib import Path

import pandas as pd

from b2b_credit_risk_analysis.warehouse.build_dim_date import build_dim_date
from b2b_credit_risk_analysis.warehouse.build_dimensions import (
    build_dim_country,
    build_dim_customer,
    build_dim_industry,
    build_dim_risk_rating,
)
from b2b_credit_risk_analysis.warehouse.build_facts import (
    build_fact_default_event,
    build_fact_exposure_snapshot,
    build_fact_invoice,
    build_fact_payment,
    build_fact_rating_history,
)
from b2b_credit_risk_analysis.warehouse.export_phase2_tables import export_phase2_tables


def load_phase1_outputs(input_dir: str = "data/processed/phase1") -> dict[str, pd.DataFrame]:
    input_path = Path(input_dir)

    files = {
        "dim_customer": input_path / "dim_customer.csv",
        "customer_month_panel": input_path / "customer_month_panel.csv",
        "fact_invoice": input_path / "fact_invoice.csv",
        "fact_payment": input_path / "fact_payment.csv",
        "fact_default_event": input_path / "fact_default_event.csv",
    }

    missing = [name for name, path in files.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing Phase 1 files in {input_path}: {missing}"
        )

    outputs = {
        name: pd.read_csv(path)
        for name, path in files.items()
    }
    return outputs


def build_phase2_tables(
    dim_customer_phase1: pd.DataFrame,
    customer_month_panel_phase1: pd.DataFrame,
    fact_invoice_phase1: pd.DataFrame,
    fact_payment_phase1: pd.DataFrame,
    fact_default_event_phase1: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    dim_date = build_dim_date(
        dim_customer=dim_customer_phase1,
        customer_month_panel=customer_month_panel_phase1,
        fact_invoice=fact_invoice_phase1,
        fact_payment=fact_payment_phase1,
        fact_default_event=fact_default_event_phase1,
    )

    dim_country = build_dim_country(dim_customer_phase1)
    dim_industry = build_dim_industry(dim_customer_phase1)
    dim_risk_rating = build_dim_risk_rating()

    dim_customer = build_dim_customer(
        dim_customer_phase1=dim_customer_phase1,
        dim_country=dim_country,
        dim_industry=dim_industry,
        dim_date=dim_date,
    )

    fact_exposure_snapshot = build_fact_exposure_snapshot(
        customer_month_panel_phase1=customer_month_panel_phase1,
        dim_risk_rating=dim_risk_rating,
    )

    fact_invoice = build_fact_invoice(fact_invoice_phase1)
    fact_payment = build_fact_payment(fact_payment_phase1)
    fact_default_event = build_fact_default_event(fact_default_event_phase1)

    fact_rating_history = build_fact_rating_history(
        customer_month_panel_phase1=customer_month_panel_phase1,
        dim_risk_rating=dim_risk_rating,
    )

    tables = {
        "dim_date": dim_date,
        "dim_country": dim_country,
        "dim_industry": dim_industry,
        "dim_risk_rating": dim_risk_rating,
        "dim_customer": dim_customer,
        "fact_exposure_snapshot": fact_exposure_snapshot,
        "fact_invoice": fact_invoice,
        "fact_payment": fact_payment,
        "fact_default_event": fact_default_event,
        "fact_rating_history": fact_rating_history,
    }
    return tables


def run_phase2(
    input_dir: str = "data/processed/phase1",
    output_dir: str = "data/processed/phase2",
    save_parquet: bool = False,
) -> dict[str, pd.DataFrame]:
    phase1 = load_phase1_outputs(input_dir=input_dir)

    phase2_tables = build_phase2_tables(
        dim_customer_phase1=phase1["dim_customer"],
        customer_month_panel_phase1=phase1["customer_month_panel"],
        fact_invoice_phase1=phase1["fact_invoice"],
        fact_payment_phase1=phase1["fact_payment"],
        fact_default_event_phase1=phase1["fact_default_event"],
    )

    export_phase2_tables(
        tables=phase2_tables,
        output_dir=output_dir,
        save_parquet=save_parquet,
    )

    print("\nPhase 2 warehouse tables created successfully.")
    for name, df in phase2_tables.items():
        print(f" - {name}: {df.shape}")

    return phase2_tables


if __name__ == "__main__":
    run_phase2()