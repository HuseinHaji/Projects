-- Fact: Default Event
CREATE TABLE IF NOT EXISTS credit_risk.fact_default_event (
  default_event_key BIGINT PRIMARY KEY,
  customer_key BIGINT NOT NULL REFERENCES credit_risk.dim_customer(customer_key),
  default_date_key INTEGER NOT NULL REFERENCES credit_risk.dim_date(date_key),
  default_date DATE NOT NULL,
  default_amount DECIMAL(15, 2) NOT NULL,
  recovery_amount DECIMAL(15, 2),
  net_loss_amount DECIMAL(15, 2),
  default_reason VARCHAR(50),
  claim_status VARCHAR(20),
  days_from_first_overdue INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fact_default_customer ON credit_risk.fact_default_event(customer_key);
CREATE INDEX idx_fact_default_date ON credit_risk.fact_default_event(default_date);
CREATE INDEX idx_fact_default_reason ON credit_risk.fact_default_event(default_reason);
COMMENT ON TABLE credit_risk.fact_default_event IS 'Default event occurrences with loss details';
