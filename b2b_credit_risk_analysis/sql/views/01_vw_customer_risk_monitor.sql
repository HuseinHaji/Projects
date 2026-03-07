-- View: Customer Risk Monitor
-- Real-time view of current risk metrics for each customer
CREATE OR REPLACE VIEW credit_risk.vw_customer_risk_monitor AS
SELECT
  dc.customer_key,
  dc.customer_id,
  dc.customer_name,
  c.country_name,
  i.industry_name,
  dc.company_size,
  dc.annual_revenue_eur,
  fes.snapshot_date,
  fes.rating_code,
  fes.rating_score,
  fes.current_exposure,
  fes.utilization_ratio,
  fes.avg_days_past_due,
  fes.overdue_ratio,
  fes.warning_flag,
  fes.stress_flag,
  CASE 
    WHEN fes.rating_score >= 6 THEN 'HIGH'
    WHEN fes.rating_score >= 5 THEN 'MEDIUM'
    ELSE 'LOW'
  END AS risk_level,
  fde.default_event_key IS NOT NULL AS has_defaulted
FROM credit_risk.dim_customer dc
LEFT JOIN credit_risk.dim_country c ON dc.country_key = c.country_key
LEFT JOIN credit_risk.dim_industry i ON dc.industry_key = i.industry_key
LEFT JOIN (
  SELECT * FROM credit_risk.fact_exposure_snapshot
  WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM credit_risk.fact_exposure_snapshot)
) fes ON dc.customer_key = fes.customer_key
LEFT JOIN credit_risk.fact_default_event fde ON dc.customer_key = fde.customer_key
WHERE dc.active_flag = true;

COMMENT ON VIEW credit_risk.vw_customer_risk_monitor IS 'Real-time risk metrics for active customers at latest snapshot';
