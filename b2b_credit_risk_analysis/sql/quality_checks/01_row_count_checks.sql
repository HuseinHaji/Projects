-- Quality Check: Row Count Validation
-- Verifies that row counts match expectations between staging and loaded tables
SELECT
  'stg_customer' AS table_name,
  COUNT(*) AS row_count,
  CURRENT_TIMESTAMP AS check_timestamp
FROM credit_risk.stg_customer
UNION ALL
SELECT
  'stg_customer_month_panel',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.stg_customer_month_panel
UNION ALL
SELECT
  'stg_invoice',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.stg_invoice
UNION ALL
SELECT
  'stg_payment',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.stg_payment
UNION ALL
SELECT
  'stg_default_event',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.stg_default_event
UNION ALL
SELECT
  'dim_customer',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.dim_customer
UNION ALL
SELECT
  'fact_invoice',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.fact_invoice
UNION ALL
SELECT
  'fact_payment',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.fact_payment
UNION ALL
SELECT
  'fact_default_event',
  COUNT(*),
  CURRENT_TIMESTAMP
FROM credit_risk.fact_default_event
ORDER BY table_name;

COMMENT ON TABLE credit_risk.stg_customer IS 'Row count check to identify data completeness';
