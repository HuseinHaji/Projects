-- Analytics: Monthly Portfolio Summary
-- Comprehensive portfolio health dashboard metrics
SELECT
  fes.year_month,
  COUNT(DISTINCT fes.customer_key) AS total_customers,
  ROUND(SUM(fes.monthly_sales_estimate), 2) AS monthly_sales_eur,
  ROUND(SUM(fes.current_exposure), 2) AS current_exposure_eur,
  ROUND(SUM(fes.overdue_exposure), 2) AS overdue_exposure_eur,
  ROUND(SUM(fes.overdue_exposure) / SUM(fes.current_exposure) * 100, 2) AS overdue_ratio_pct,
  ROUND(AVG(fes.utilization_ratio), 4) AS avg_utilization,
  ROUND(AVG(fes.avg_days_past_due), 2) AS avg_dpd,
  COUNT(CASE WHEN fes.warning_flag THEN 1 END) AS customers_with_warnings,
  COUNT(CASE WHEN fes.stress_flag THEN 1 END) AS customers_under_stress,
  COUNT(CASE WHEN fes.default_in_next_90d THEN 1 END) AS customers_at_default_risk
FROM credit_risk.fact_exposure_snapshot fes
GROUP BY fes.year_month
ORDER BY fes.year_month DESC;
