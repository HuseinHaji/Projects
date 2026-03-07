-- Dimension: Risk Rating
CREATE TABLE IF NOT EXISTS credit_risk.dim_risk_rating (
  rating_key SERIAL PRIMARY KEY,
  rating_code VARCHAR(10) UNIQUE NOT NULL,
  rating_score SMALLINT NOT NULL,
  rating_category VARCHAR(50) NOT NULL,
  risk_tier VARCHAR(20) NOT NULL,
  pdo_annual_pct DECIMAL(5, 2),
  lgd_pct DECIMAL(5, 2),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE credit_risk.dim_risk_rating IS 'Risk rating dimension with PD/LGD parameters';
