-- Load: Fact Exposure Snapshot
-- Loads monthly exposure snapshot from staging
INSERT INTO credit_risk.fact_exposure_snapshot (
  exposure_snapshot_key, customer_key, date_key, snapshot_date, year_month,
  monthly_sales_estimate, invoice_count_month, current_exposure, overdue_exposure,
  overdue_ratio, insured_limit, utilization_ratio, avg_days_past_due,
  max_days_past_due, open_invoice_count, rating_code, rating_score,
  notch_change, downgrade_flag, stress_flag, warning_flag,
  default_in_next_90d, is_defaulted
)
SELECT
  ROW_NUMBER() OVER (ORDER BY scmp.customer_key, scmp.snapshot_date),
  scmp.customer_key,
  dd.date_key,
  scmp.snapshot_date,
  scmp.year_month,
  scmp.monthly_sales_estimate,
  scmp.invoice_count_month,
  scmp.current_exposure,
  scmp.overdue_exposure,
  scmp.overdue_ratio,
  scmp.insured_limit,
  scmp.utilization_ratio,
  scmp.avg_days_past_due,
  scmp.max_days_past_due,
  scmp.open_invoice_count,
  scmp.rating_code,
  scmp.rating_score,
  scmp.notch_change,
  scmp.downgrade_flag,
  scmp.stress_flag,
  scmp.warning_flag,
  scmp.default_in_next_90d,
  scmp.is_defaulted
FROM credit_risk.stg_customer_month_panel scmp
LEFT JOIN credit_risk.dim_date dd ON scmp.snapshot_date = dd.date_id
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.fact_exposure_snapshot fes 
  WHERE fes.customer_key = scmp.customer_key 
    AND fes.snapshot_date = scmp.snapshot_date
);

COMMENT ON TABLE credit_risk.fact_exposure_snapshot IS 'Monthly exposure snapshot fact loaded from staging';
