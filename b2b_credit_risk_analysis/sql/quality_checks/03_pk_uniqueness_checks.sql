SELECT 'dim_customer.customer_key' AS check_name, customer_key, COUNT(*)
FROM credit_risk_dw.dim_customer
GROUP BY customer_key
HAVING COUNT(*) > 1

UNION ALL

SELECT 'fact_invoice.invoice_key', invoice_key::integer, COUNT(*)
FROM credit_risk_dw.fact_invoice
GROUP BY invoice_key
HAVING COUNT(*) > 1;

SELECT customer_key, COUNT(*)
FROM credit_risk_dw.dim_customer
GROUP BY customer_key
HAVING COUNT(*) > 1;

SELECT invoice_key, COUNT(*)
FROM credit_risk_dw.fact_invoice
GROUP BY invoice_key
HAVING COUNT(*) > 1;

SELECT payment_key, COUNT(*)
FROM credit_risk_dw.fact_payment
GROUP BY payment_key
HAVING COUNT(*) > 1;

SELECT default_event_key, COUNT(*)
FROM credit_risk_dw.fact_default_event
GROUP BY default_event_key
HAVING COUNT(*) > 1;

SELECT exposure_snapshot_key, COUNT(*)
FROM credit_risk_dw.fact_exposure_snapshot
GROUP BY exposure_snapshot_key
HAVING COUNT(*) > 1;

SELECT rating_history_key, COUNT(*)
FROM credit_risk_dw.fact_rating_history
GROUP BY rating_history_key
HAVING COUNT(*) > 1;