SELECT COUNT(*) AS missing_exp_customer_fk
FROM credit_risk_dw.fact_exposure_snapshot f
LEFT JOIN credit_risk_dw.dim_customer d
    ON f.customer_key = d.customer_key
WHERE d.customer_key IS NULL;

SELECT COUNT(*) AS missing_exp_date_fk
FROM credit_risk_dw.fact_exposure_snapshot f
LEFT JOIN credit_risk_dw.dim_date d
    ON f.snapshot_date_key = d.date_key
WHERE d.date_key IS NULL;

SELECT COUNT(*) AS missing_exp_rating_fk
FROM credit_risk_dw.fact_exposure_snapshot f
LEFT JOIN credit_risk_dw.dim_risk_rating r
    ON f.rating_key = r.rating_key
WHERE r.rating_key IS NULL;

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

SELECT COUNT(*) AS missing_rating_hist_customer_fk
FROM credit_risk_dw.fact_rating_history f
LEFT JOIN credit_risk_dw.dim_customer d
    ON f.customer_key = d.customer_key
WHERE d.customer_key IS NULL;