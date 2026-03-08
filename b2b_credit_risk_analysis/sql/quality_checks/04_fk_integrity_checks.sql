-- Quality Check: Foreign Key Integrity
-- Validates referential integrity between fact and dimension tables
SELECT COUNT(*) AS missing_exp_customer_fk
FROM credit_risk_dw.fact_exposure_snapshot f
LEFT JOIN credit_risk_dw.dim_customer d
    ON f.customer_key = d.customer_key
WHERE d.customer_key IS NULL;

SELECT COUNT(*) AS missing_invoice_customer_fk
FROM credit_risk_dw.fact_invoice f
LEFT JOIN credit_risk_dw.dim_customer d
    ON f.customer_key = d.customer_key
WHERE d.customer_key IS NULL;

SELECT COUNT(*) AS missing_payment_invoice_fk
FROM credit_risk_dw.fact_payment p
LEFT JOIN credit_risk_dw.fact_invoice i
    ON p.invoice_key = i.invoice_key
WHERE i.invoice_key IS NULL;

SELECT COUNT(*) AS missing_default_customer_fk
FROM credit_risk_dw.fact_default_event f
LEFT JOIN credit_risk_dw.dim_customer d
    ON f.customer_key = d.customer_key
WHERE d.customer_key IS NULL;