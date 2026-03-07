-- Fact: Rating History
CREATE TABLE IF NOT EXISTS credit_risk.fact_rating_history (
  rating_history_key BIGINT PRIMARY KEY,
  customer_key BIGINT NOT NULL REFERENCES credit_risk.dim_customer(customer_key),
  rating_key INTEGER NOT NULL REFERENCES credit_risk.dim_risk_rating(rating_key),
  date_key INTEGER NOT NULL REFERENCES credit_risk.dim_date(date_key),
  rating_date DATE NOT NULL,
  rating_code VARCHAR(10) NOT NULL,
  rating_score SMALLINT NOT NULL,
  previous_rating_code VARCHAR(10),
  previous_rating_score SMALLINT,
  notch_change SMALLINT,
  reason_for_change VARCHAR(100),
  is_downgrade BOOLEAN DEFAULT false,
  is_upgrade BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fact_rating_customer ON credit_risk.fact_rating_history(customer_key);
CREATE INDEX idx_fact_rating_date ON credit_risk.fact_rating_history(rating_date);
CREATE INDEX idx_fact_rating_code ON credit_risk.fact_rating_history(rating_code);
COMMENT ON TABLE credit_risk.fact_rating_history IS 'Historical rating changes and transitions';
