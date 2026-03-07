-- Analytics: Exposure by Country and Industry
-- Portfolio concentration analysis
SELECT
  c.country_name,
  i.industry_name,
  COUNT(DISTINCT fes.customer_key) AS customers,
  ROUND(SUM(fes.current_exposure), 2) AS total_exposure_eur,
  ROUND(SUM(fes.current_exposure) / SUM(SUM(fes.current_exposure)) OVER () * 100, 2) AS portfolio_share_pct,
  ROUND(AVG(fes.utilization_ratio), 4) AS avg_utilization,
  ROUND(AVG(fes.avg_days_past_due), 2) AS avg_dpd,
  COUNT(CASE WHEN fes.rating_score >= 6 THEN 1 END) AS high_risk_customers
FROM credit_risk.fact_exposure_snapshot fes
LEFT JOIN credit_risk.dim_customer dc ON fes.customer_key = dc.customer_key
LEFT JOIN credit_risk.dim_country c ON dc.country_key = c.country_key
LEFT JOIN credit_risk.dim_industry i ON dc.industry_key = i.industry_key
WHERE fes.snapshot_date = (SELECT MAX(snapshot_date) FROM credit_risk.fact_exposure_snapshot)
GROUP BY c.country_name, i.industry_name
ORDER BY total_exposure_eur DESC;
