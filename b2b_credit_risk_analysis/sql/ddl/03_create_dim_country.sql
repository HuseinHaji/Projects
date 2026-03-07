-- Dimension: Country
CREATE TABLE IF NOT EXISTS credit_risk.dim_country (
  country_key SERIAL PRIMARY KEY,
  country_code VARCHAR(2) UNIQUE NOT NULL,
  country_name VARCHAR(100) NOT NULL,
  region VARCHAR(50),
  gdp_usd DECIMAL(15, 2),
  gdp_growth_pct DECIMAL(5, 2),
  unemployment_rate_pct DECIMAL(5, 2),
  inflation_rate_pct DECIMAL(5, 2),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_country_code ON credit_risk.dim_country(country_code);
COMMENT ON TABLE credit_risk.dim_country IS 'Country dimension with macroeconomic indicators';
