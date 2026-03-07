-- Quality Check: Business Rule Validation
-- Validates domain-specific rules and data consistency
SELECT
  'Invoice amount must be > 0' AS rule_name,
  COUNT(*) AS violations
FROM credit_risk.fact_invoice
WHERE invoice_amount <= 0
UNION ALL
SELECT
  'Payment amount must be > 0',
  COUNT(*)
FROM credit_risk.fact_payment
WHERE payment_amount <= 0
UNION ALL
SELECT
  'Due date must be >= invoice date',
  COUNT(*)
FROM credit_risk.fact_invoice
WHERE due_date < invoice_date
UNION ALL
SELECT
  'Utilization ratio must be between 0 and 1.5',
  COUNT(*)
FROM credit_risk.fact_exposure_snapshot
WHERE utilization_ratio < 0 OR utilization_ratio > 1.5
UNION ALL
SELECT
  'Overdue ratio must be between 0 and 1',
  COUNT(*)
FROM credit_risk.fact_exposure_snapshot
WHERE overdue_ratio < 0 OR overdue_ratio > 1
UNION ALL
SELECT
  'DPD (Days Past Due) cannot be negative',
  COUNT(*)
FROM credit_risk.fact_exposure_snapshot
WHERE avg_days_past_due < 0
ORDER BY rule_name;

COMMENT ON TABLE credit_risk.fact_invoice IS 'Validate business rules and domain constraints';
