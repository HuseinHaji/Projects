-- Fact: Exposure Snapshot (Monthly Panel)
CREATE TABLE IF NOT EXISTS credit_risk.fact_exposure_snapshot (
  exposure_snapshot_key BIGINT PRIMARY KEY,
  customer_key BIGINT NOT NULL REFERENCES credit_risk.dim_customer(customer_key),
  date_key INTEGER NOT NULL REFERENCES credit_risk.dim_date(date_key),
  snapshot_date DATE NOT NULL,
  year_month VARCHAR(7) NOT NULL,
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
  downgrade_flag BOOLEAN DEFAULT false,
  stress_flag BOOLEAN DEFAULT false,
  warning_flag BOOLEAN DEFAULT false,
  default_in_next_90d BOOLEAN DEFAULT false,
  is_defaulted BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fact_exposure_customer ON credit_risk.fact_exposure_snapshot(customer_key);
CREATE INDEX idx_fact_exposure_date ON credit_risk.fact_exposure_snapshot(snapshot_date);
CREATE INDEX idx_fact_exposure_warning ON credit_risk.fact_exposure_snapshot(warning_flag);
COMMENT ON TABLE credit_risk.fact_exposure_snapshot IS 'Monthly exposure and risk metrics per customer';
