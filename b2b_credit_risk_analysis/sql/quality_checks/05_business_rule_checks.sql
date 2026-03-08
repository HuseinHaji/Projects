-- Quality Check: Business Rule Validation
-- Validates domain-specific rules and data consistency
SELECT COUNT(*) AS invalid_overdue_rows
FROM credit_risk_dw.fact_exposure_snapshot
WHERE overdue_exposure > current_exposure;

SELECT COUNT(*) AS invalid_recovery_rows
FROM credit_risk_dw.fact_default_event
WHERE recovery_amount > default_amount;

SELECT COUNT(*) AS invalid_invoice_date_order
FROM credit_risk_dw.fact_invoice
WHERE due_date_key < invoice_date_key;

SELECT COUNT(*) AS invalid_negative_payment_amount
FROM credit_risk_dw.fact_payment
WHERE payment_amount <= 0;
