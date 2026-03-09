SELECT 'dim_date' AS table_name, COUNT(*) AS row_count
FROM credit_risk_dw.dim_date
UNION ALL
SELECT 'dim_country', COUNT(*) FROM credit_risk_dw.dim_country
UNION ALL
SELECT 'dim_industry', COUNT(*) FROM credit_risk_dw.dim_industry
UNION ALL
SELECT 'dim_risk_rating', COUNT(*) FROM credit_risk_dw.dim_risk_rating
UNION ALL
SELECT 'dim_customer', COUNT(*) FROM credit_risk_dw.dim_customer
UNION ALL
SELECT 'fact_exposure_snapshot', COUNT(*) FROM credit_risk_dw.fact_exposure_snapshot
UNION ALL
SELECT 'fact_invoice', COUNT(*) FROM credit_risk_dw.fact_invoice
UNION ALL
SELECT 'fact_payment', COUNT(*) FROM credit_risk_dw.fact_payment
UNION ALL
SELECT 'fact_default_event', COUNT(*) FROM credit_risk_dw.fact_default_event
UNION ALL
SELECT 'fact_rating_history', COUNT(*) FROM credit_risk_dw.fact_rating_history
ORDER BY table_name;