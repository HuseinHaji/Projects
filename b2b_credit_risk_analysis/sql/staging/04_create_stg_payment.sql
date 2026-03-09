-- Staging: Payment
-- Loads raw payment transaction data from CSV exports
CREATE TABLE IF NOT EXISTS credit_risk.stg_payment (
  payment_key BIGINT,
  payment_id VARCHAR(50),
  invoice_key BIGINT,
  customer_key BIGINT,
  payment_date DATE,
  payment_amount DECIMAL(15, 2),
  currency_code VARCHAR(3),
  payment_method VARCHAR(50),
  load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stg_pay_invoice ON credit_risk.stg_payment(invoice_key);
CREATE INDEX idx_stg_pay_customer ON credit_risk.stg_payment(customer_key);
CREATE INDEX idx_stg_pay_date ON credit_risk.stg_payment(payment_date);
COMMENT ON TABLE credit_risk.stg_payment IS 'Staging table for raw payment transactions from CSV export';
