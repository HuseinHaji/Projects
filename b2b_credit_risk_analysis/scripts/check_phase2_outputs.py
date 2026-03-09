from b2b_credit_risk_analysis.warehouse.run_phase2 import run_phase2


def main():
    tables = run_phase2(
        input_dir="b2b_credit_risk_analysis/data/processed/phase1",
        output_dir="b2b_credit_risk_analysis/data/processed/phase2",
        save_parquet=False,
    )

    fact_exposure_snapshot = tables["fact_exposure_snapshot"]
    fact_rating_history = tables["fact_rating_history"]
    dim_customer = tables["dim_customer"]
    fact_invoice = tables["fact_invoice"]
    fact_payment = tables["fact_payment"]

    print("fact_exposure_snapshot.shape:", fact_exposure_snapshot.shape)
    print("fact_rating_history.shape:", fact_rating_history.shape)

    print("dim_customer rows:", len(dim_customer))
    print("dim_customer unique customer_key:", dim_customer["customer_key"].nunique())

    print("fact_invoice rows:", len(fact_invoice))
    print("fact_invoice unique invoice_key:", fact_invoice["invoice_key"].nunique())

    print("fact_payment rows:", len(fact_payment))
    print("all payment invoice_keys exist in fact_invoice:",
        fact_payment["invoice_key"].isin(fact_invoice["invoice_key"]).all())


if __name__ == "__main__":
    main()