CREATE OR REPLACE VIEW credit_risk_dw.vw_customer_risk_monitor AS
SELECT
    dc.customer_id,
    dc.customer_name,
    co.country_name,
    di.industry_name,
    dd.full_date AS snapshot_date,
    rr.rating_code,
    rr.rating_bucket,
    fes.current_exposure,
    fes.overdue_exposure,
    fes.overdue_ratio,
    fes.insured_limit,
    fes.utilization_ratio,
    fes.avg_days_past_due,
    fes.max_days_past_due,
    fes.open_invoice_count,
    fes.notch_change,
    fes.downgrade_flag,
    fes.stress_flag,
    fes.warning_flag,
    fes.default_in_next_90d,
    fes.is_defaulted
FROM credit_risk_dw.fact_exposure_snapshot fes
JOIN credit_risk_dw.dim_customer dc
    ON fes.customer_key = dc.customer_key
JOIN credit_risk_dw.dim_country co
    ON dc.country_key = co.country_key
JOIN credit_risk_dw.dim_industry di
    ON dc.industry_key = di.industry_key
JOIN credit_risk_dw.dim_date dd
    ON fes.snapshot_date_key = dd.date_key
JOIN credit_risk_dw.dim_risk_rating rr
    ON fes.rating_key = rr.rating_key;