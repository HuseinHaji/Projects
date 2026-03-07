-- Quality Check: Primary Key Uniqueness
-- Validates that primary keys are unique and not NULL
SELECT
  'dim_customer_key' AS check_name,
  COUNT(*) - COUNT(DISTINCT customer_key) AS duplicate_count
FROM credit_risk.dim_customer
UNION ALL
SELECT
  'fact_invoice_key',
  COUNT(*) - COUNT(DISTINCT invoice_key)
FROM credit_risk.fact_invoice
UNION ALL
SELECT
  'fact_payment_key',
  COUNT(*) - COUNT(DISTINCT payment_key)
FROM credit_risk.fact_payment
UNION ALL
SELECT
  'fact_default_event_key',
  COUNT(*) - COUNT(DISTINCT default_event_key)
FROM credit_risk.fact_default_event
UNION ALL
SELECT
  'dim_country_key',
  COUNT(*) - COUNT(DISTINCT country_key)
FROM credit_risk.dim_country
UNION ALL
SELECT
  'dim_industry_key',
  COUNT(*) - COUNT(DISTINCT industry_key)
FROM credit_risk.dim_industry
ORDER BY check_name;

COMMENT ON TABLE credit_risk.dim_customer IS 'Verify primary key uniqueness across all tables';
