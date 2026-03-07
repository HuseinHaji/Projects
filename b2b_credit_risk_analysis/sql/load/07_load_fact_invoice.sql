-- Load: Fact Invoice
-- Loads invoice transactions from staging
INSERT INTO credit_risk.fact_invoice (
  invoice_key, invoice_id, customer_key, invoice_date_key, due_date_key,
  invoice_date, due_date, invoice_amount, currency_code, payment_terms_days,
  product_category, insured_flag, invoice_status, snapshot_month
)
SELECT
  si.invoice_key,
  si.invoice_id,
  si.customer_key,
  dd1.date_key,
  dd2.date_key,
  si.invoice_date,
  si.due_date,
  si.invoice_amount,
  si.currency_code,
  si.payment_terms_days,
  si.product_category,
  si.insured_flag,
  si.invoice_status,
  si.snapshot_month
FROM credit_risk.stg_invoice si
LEFT JOIN credit_risk.dim_date dd1 ON si.invoice_date = dd1.date_id
LEFT JOIN credit_risk.dim_date dd2 ON si.due_date = dd2.date_id
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.fact_invoice fi 
  WHERE fi.invoice_key = si.invoice_key
);

COMMENT ON TABLE credit_risk.fact_invoice IS 'Invoice transactions loaded from staging';
