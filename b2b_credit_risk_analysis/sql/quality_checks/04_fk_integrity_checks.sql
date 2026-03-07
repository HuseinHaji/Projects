-- Quality Check: Foreign Key Integrity
-- Validates referential integrity between fact and dimension tables
SELECT
  'fact_invoice -> dim_customer' AS fk_check,
  COUNT(*) AS orphaned_records
FROM credit_risk.fact_invoice fi
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.dim_customer dc 
  WHERE dc.customer_key = fi.customer_key
)
UNION ALL
SELECT
  'fact_payment -> fact_invoice',
  COUNT(*)
FROM credit_risk.fact_payment fp
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.fact_invoice fi 
  WHERE fi.invoice_key = fp.invoice_key
)
UNION ALL
SELECT
  'fact_default_event -> dim_customer',
  COUNT(*)
FROM credit_risk.fact_default_event fde
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.dim_customer dc 
  WHERE dc.customer_key = fde.customer_key
)
UNION ALL
SELECT
  'fact_exposure_snapshot -> dim_customer',
  COUNT(*)
FROM credit_risk.fact_exposure_snapshot fes
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.dim_customer dc 
  WHERE dc.customer_key = fes.customer_key
)
ORDER BY fk_check;

COMMENT ON TABLE credit_risk.fact_invoice IS 'Detect orphaned records violating foreign key constraints';
