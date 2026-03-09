TRUNCATE TABLE credit_risk_dw.fact_exposure_snapshot RESTART IDENTITY CASCADE;

COPY credit_risk_dw.fact_exposure_snapshot (
    exposure_snapshot_key,
    customer_key,
    snapshot_date_key,
    rating_key,
    monthly_sales_estimate,
    invoice_count_month,
    current_exposure,
    overdue_exposure,
    overdue_ratio,
    insured_limit,
    utilization_ratio,
    avg_days_past_due,
    max_days_past_due,
    open_invoice_count,
    notch_change,
    downgrade_flag,
    stress_flag,
    warning_flag,
    default_in_next_90d,
    is_defaulted
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/fact_exposure_snapshot.csv'
DELIMITER ','
CSV HEADER;