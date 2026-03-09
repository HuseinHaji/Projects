SELECT 'dim_customer.customer_id' AS check_name, COUNT(*) AS null_count
FROM credit_risk_dw.dim_customer
WHERE customer_id IS NULL
UNION ALL
SELECT 'dim_customer.customer_name', COUNT(*)
FROM credit_risk_dw.dim_customer
WHERE customer_name IS NULL
UNION ALL
SELECT 'fact_exposure_snapshot.customer_key', COUNT(*)
FROM credit_risk_dw.fact_exposure_snapshot
WHERE customer_key IS NULL
UNION ALL
SELECT 'fact_invoice.invoice_id', COUNT(*)
FROM credit_risk_dw.fact_invoice
WHERE invoice_id IS NULL
UNION ALL
SELECT 'fact_payment.invoice_key', COUNT(*)
FROM credit_risk_dw.fact_payment
WHERE invoice_key IS NULL
UNION ALL
SELECT 'fact_default_event.customer_key', COUNT(*)
FROM credit_risk_dw.fact_default_event
WHERE customer_key IS NULL;