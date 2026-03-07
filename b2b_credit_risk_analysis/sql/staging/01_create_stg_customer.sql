-- Staging: Customer dimension
-- Loads raw customer data from CSV exports
CREATE TABLE IF NOT EXISTS credit_risk.stg_customer (
  customer_key BIGINT,
  customer_id VARCHAR(20),
  customer_name VARCHAR(255),
  country VARCHAR(100),
  industry VARCHAR(100),
  company_size VARCHAR(20),
  years_in_business SMALLINT,
  annual_revenue_eur DECIMAL(15, 2),
  employee_count INTEGER,
  legal_form VARCHAR(50),
  parent_group_flag BOOLEAN,
  base_risk_score DECIMAL(5, 3),
  base_insured_limit DECIMAL(15, 2),
  onboarding_date DATE,
  active_flag BOOLEAN,
  load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE credit_risk.stg_customer IS 'Staging table for raw customer data from CSV export';
