-- Quality Check: NULL Value Validation
-- Detects unexpected NULL values in critical columns
SELECT
  'dim_customer - NULL customer_id' AS check_name,
  COUNT(*) AS null_count
FROM credit_risk.dim_customer
WHERE customer_id IS NULL
UNION ALL
SELECT
  'dim_customer - NULL annual_revenue_eur',
  COUNT(*)
FROM credit_risk.dim_customer
WHERE annual_revenue_eur IS NULL
UNION ALL
SELECT
  'fact_invoice - NULL invoice_amount',
  COUNT(*)
FROM credit_risk.fact_invoice
WHERE invoice_amount IS NULL
UNION ALL
SELECT
  'fact_invoice - NULL due_date',
  COUNT(*)
FROM credit_risk.fact_invoice
WHERE due_date IS NULL
UNION ALL
SELECT
  'fact_payment - NULL payment_amount',
  COUNT(*)
FROM credit_risk.fact_payment
WHERE payment_amount IS NULL
UNION ALL
SELECT
  'fact_exposure_snapshot - NULL current_exposure',
  COUNT(*)
FROM credit_risk.fact_exposure_snapshot
WHERE current_exposure IS NULL
ORDER BY check_name;

COMMENT ON TABLE credit_risk.dim_customer IS 'Identify NULL values in key columns that should be NOT NULL';
