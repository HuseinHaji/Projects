-- Dimension: Industry
CREATE TABLE IF NOT EXISTS credit_risk.dim_industry (
  industry_key SERIAL PRIMARY KEY,
  industry_code VARCHAR(10) UNIQUE NOT NULL,
  industry_name VARCHAR(100) NOT NULL,
  sector VARCHAR(50),
  avg_payment_terms_days SMALLINT,
  avg_invoice_size_eur DECIMAL(12, 2),
  insolvency_rate_pct DECIMAL(5, 2),
  volatility_score DECIMAL(3, 2),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_industry_code ON credit_risk.dim_industry(industry_code);
COMMENT ON TABLE credit_risk.dim_industry IS 'Industry dimension with sector-level metrics';
