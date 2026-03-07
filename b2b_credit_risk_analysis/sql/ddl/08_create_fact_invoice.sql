-- Fact: Invoice
CREATE TABLE IF NOT EXISTS credit_risk.fact_invoice (
  invoice_key BIGINT PRIMARY KEY,
  invoice_id VARCHAR(50) NOT NULL,
  customer_key BIGINT NOT NULL REFERENCES credit_risk.dim_customer(customer_key),
  invoice_date_key INTEGER NOT NULL REFERENCES credit_risk.dim_date(date_key),
  due_date_key INTEGER NOT NULL REFERENCES credit_risk.dim_date(date_key),
  invoice_date DATE NOT NULL,
  due_date DATE NOT NULL,
  invoice_amount DECIMAL(15, 2) NOT NULL,
  currency_code VARCHAR(3) DEFAULT 'EUR',
  payment_terms_days SMALLINT,
  product_category VARCHAR(100),
  insured_flag BOOLEAN DEFAULT true,
  invoice_status VARCHAR(20),
  snapshot_month VARCHAR(7),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fact_invoice_customer ON credit_risk.fact_invoice(customer_key);
CREATE INDEX idx_fact_invoice_date ON credit_risk.fact_invoice(invoice_date);
CREATE INDEX idx_fact_invoice_due ON credit_risk.fact_invoice(due_date);
CREATE INDEX idx_fact_invoice_status ON credit_risk.fact_invoice(invoice_status);
COMMENT ON TABLE credit_risk.fact_invoice IS 'Individual invoice transactions';
