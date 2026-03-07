-- Dimension: Customer
CREATE TABLE IF NOT EXISTS credit_risk.dim_customer (
  customer_key BIGINT PRIMARY KEY,
  customer_id VARCHAR(20) NOT NULL,
  customer_name VARCHAR(255) NOT NULL,
  country_key INTEGER NOT NULL REFERENCES credit_risk.dim_country(country_key),
  industry_key INTEGER NOT NULL REFERENCES credit_risk.dim_industry(industry_key),
  company_size VARCHAR(20) NOT NULL,
  years_in_business SMALLINT,
  annual_revenue_eur DECIMAL(15, 2),
  employee_count INTEGER,
  legal_form VARCHAR(50),
  parent_group_flag BOOLEAN DEFAULT false,
  base_risk_score DECIMAL(5, 3),
  base_insured_limit DECIMAL(15, 2),
  onboarding_date DATE,
  active_flag BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_customer_id ON credit_risk.dim_customer(customer_id);
CREATE INDEX idx_dim_customer_country ON credit_risk.dim_customer(country_key);
CREATE INDEX idx_dim_customer_industry ON credit_risk.dim_customer(industry_key);
COMMENT ON TABLE credit_risk.dim_customer IS 'Master customer dimension with profile and risk attributes';
