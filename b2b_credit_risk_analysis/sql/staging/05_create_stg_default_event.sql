-- Staging: Default Event
-- Loads raw default event data from CSV exports
CREATE TABLE IF NOT EXISTS credit_risk.stg_default_event (
  default_event_key BIGINT,
  customer_key BIGINT,
  default_date DATE,
  default_amount DECIMAL(15, 2),
  recovery_amount DECIMAL(15, 2),
  net_loss_amount DECIMAL(15, 2),
  default_reason VARCHAR(50),
  claim_status VARCHAR(20),
  days_from_first_overdue INTEGER,
  load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stg_def_customer ON credit_risk.stg_default_event(customer_key);
CREATE INDEX idx_stg_def_date ON credit_risk.stg_default_event(default_date);
COMMENT ON TABLE credit_risk.stg_default_event IS 'Staging table for raw default events from CSV export';
