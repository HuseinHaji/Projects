-- Analytics: Overdue Trend
-- Time series analysis of overdue exposure and ratio
SELECT
  fes.year_month,
  ROUND(SUM(fes.current_exposure), 2) AS total_exposure_eur,
  ROUND(SUM(fes.overdue_exposure), 2) AS overdue_exposure_eur,
  ROUND(SUM(fes.overdue_exposure) / SUM(fes.current_exposure) * 100, 2) AS overdue_ratio_pct,
  ROUND(AVG(fes.avg_days_past_due), 2) AS avg_days_overdue,
  COUNT(DISTINCT CASE WHEN fes.overdue_exposure > 0 THEN fes.customer_key END) AS customers_with_overdue,
  COUNT(DISTINCT CASE WHEN fes.avg_days_past_due >= 90 THEN fes.customer_key END) AS customers_90_plus_dpd
FROM credit_risk.fact_exposure_snapshot fes
GROUP BY fes.year_month
ORDER BY fes.year_month;
