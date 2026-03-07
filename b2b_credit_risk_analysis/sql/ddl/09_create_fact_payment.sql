-- Fact: Payment
CREATE TABLE IF NOT EXISTS credit_risk.fact_payment (
  payment_key BIGINT PRIMARY KEY,
  payment_id VARCHAR(50) NOT NULL,
  invoice_key BIGINT NOT NULL REFERENCES credit_risk.fact_invoice(invoice_key),
  customer_key BIGINT NOT NULL REFERENCES credit_risk.dim_customer(customer_key),
  payment_date_key INTEGER NOT NULL REFERENCES credit_risk.dim_date(date_key),
  payment_date DATE NOT NULL,
  payment_amount DECIMAL(15, 2) NOT NULL,
  currency_code VARCHAR(3) DEFAULT 'EUR',
  payment_method VARCHAR(50),
  is_on_time BOOLEAN,
  days_late SMALLINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fact_payment_invoice ON credit_risk.fact_payment(invoice_key);
CREATE INDEX idx_fact_payment_customer ON credit_risk.fact_payment(customer_key);
CREATE INDEX idx_fact_payment_date ON credit_risk.fact_payment(payment_date);
COMMENT ON TABLE credit_risk.fact_payment IS 'Individual payment transactions';
