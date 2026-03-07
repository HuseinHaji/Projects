-- Analytics: Top Risk Accounts
-- Identifies highest-risk customers by exposure and warning signals
SELECT
  dc.customer_id,
  dc.customer_name,
  c.country_name,
  i.industry_name,
  fes.rating_code,
  fes.current_exposure,
  fes.overdue_exposure,
  fes.utilization_ratio,
  fes.avg_days_past_due,
  fes.warning_flag,
  fes.stress_flag,
  fes.default_in_next_90d,
  CASE 
    WHEN fes.default_in_next_90d THEN 'CRITICAL'
    WHEN fes.stress_flag AND fes.warning_flag THEN 'HIGH'
    WHEN fes.stress_flag OR fes.warning_flag THEN 'MEDIUM'
    ELSE 'LOW'
  END AS alert_level,
  fes.snapshot_date
FROM credit_risk.fact_exposure_snapshot fes
LEFT JOIN credit_risk.dim_customer dc ON fes.customer_key = dc.customer_key
LEFT JOIN credit_risk.dim_country c ON dc.country_key = c.country_key
LEFT JOIN credit_risk.dim_industry i ON dc.industry_key = i.industry_key
WHERE fes.snapshot_date = (SELECT MAX(snapshot_date) FROM credit_risk.fact_exposure_snapshot)
  AND (fes.warning_flag OR fes.stress_flag OR fes.default_in_next_90d)
ORDER BY 
  CASE 
    WHEN fes.default_in_next_90d THEN 1
    WHEN fes.stress_flag AND fes.warning_flag THEN 2
    WHEN fes.stress_flag OR fes.warning_flag THEN 3
    ELSE 4
  END,
  fes.current_exposure DESC
LIMIT 100;
