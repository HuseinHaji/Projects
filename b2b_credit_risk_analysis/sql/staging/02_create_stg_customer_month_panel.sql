-- Staging: Customer Month Panel
-- Loads raw monthly customer panel data from CSV exports
CREATE TABLE IF NOT EXISTS credit_risk.stg_customer_month_panel (
  customer_key BIGINT,
  snapshot_date DATE,
  year_month VARCHAR(7),
  monthly_sales_estimate DECIMAL(12, 2),
  invoice_count_month INTEGER,
  current_exposure DECIMAL(15, 2),
  overdue_exposure DECIMAL(15, 2),
  overdue_ratio DECIMAL(5, 4),
  insured_limit DECIMAL(15, 2),
  utilization_ratio DECIMAL(5, 4),
  avg_days_past_due DECIMAL(8, 2),
  max_days_past_due INTEGER,
  open_invoice_count INTEGER,
  rating_code VARCHAR(10),
  rating_score SMALLINT,
  notch_change SMALLINT,
  downgrade_flag BOOLEAN,
  stress_flag BOOLEAN,
  warning_flag BOOLEAN,
  default_in_next_90d BOOLEAN,
  is_defaulted BOOLEAN,
  load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stg_cmp_customer ON credit_risk.stg_customer_month_panel(customer_key);
CREATE INDEX idx_stg_cmp_snapshot ON credit_risk.stg_customer_month_panel(snapshot_date);
COMMENT ON TABLE credit_risk.stg_customer_month_panel IS 'Staging table for raw monthly customer metrics from CSV export';
