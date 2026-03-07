-- Staging: Invoice
-- Loads raw invoice transaction data from CSV exports
CREATE TABLE IF NOT EXISTS credit_risk.stg_invoice (
  invoice_key BIGINT,
  invoice_id VARCHAR(50),
  customer_key BIGINT,
  invoice_date DATE,
  due_date DATE,
  invoice_amount DECIMAL(15, 2),
  currency_code VARCHAR(3),
  payment_terms_days SMALLINT,
  product_category VARCHAR(100),
  insured_flag BOOLEAN,
  invoice_status VARCHAR(20),
  snapshot_month VARCHAR(7),
  load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stg_inv_customer ON credit_risk.stg_invoice(customer_key);
CREATE INDEX idx_stg_inv_date ON credit_risk.stg_invoice(invoice_date);
COMMENT ON TABLE credit_risk.stg_invoice IS 'Staging table for raw invoice transactions from CSV export';
