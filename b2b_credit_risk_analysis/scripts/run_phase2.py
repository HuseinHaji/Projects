from b2b_credit_risk_analysis.warehouse.run_phase2 import run_phase2


if __name__ == "__main__":
    run_phase2(
        input_dir="data/processed/phase1",
        output_dir="data/processed/phase2",
        save_parquet=False,
    )