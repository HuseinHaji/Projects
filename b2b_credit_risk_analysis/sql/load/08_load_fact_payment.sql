-- Load: Fact Payment
-- Loads payment transactions from staging
INSERT INTO credit_risk.fact_payment (
  payment_key, payment_id, invoice_key, customer_key, payment_date_key,
  payment_date, payment_amount, currency_code, payment_method,
  is_on_time, days_late
)
SELECT
  sp.payment_key,
  sp.payment_id,
  sp.invoice_key,
  sp.customer_key,
  dd.date_key,
  sp.payment_date,
  sp.payment_amount,
  sp.currency_code,
  sp.payment_method,
  sp.payment_date <= fi.due_date AS is_on_time,
  EXTRACT(DAY FROM sp.payment_date - fi.due_date)::SMALLINT AS days_late
FROM credit_risk.stg_payment sp
LEFT JOIN credit_risk.dim_date dd ON sp.payment_date = dd.date_id
LEFT JOIN credit_risk.fact_invoice fi ON sp.invoice_key = fi.invoice_key
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.fact_payment fp 
  WHERE fp.payment_key = sp.payment_key
);

COMMENT ON TABLE credit_risk.fact_payment IS 'Payment transactions loaded from staging with on-time indicator';
