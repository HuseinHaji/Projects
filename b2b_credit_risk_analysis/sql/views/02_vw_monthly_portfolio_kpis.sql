-- View: Monthly Portfolio KPIs
-- Aggregated portfolio metrics by month
CREATE OR REPLACE VIEW credit_risk.vw_monthly_portfolio_kpis AS
SELECT
  fes.year_month,
  COUNT(DISTINCT fes.customer_key) AS active_customers,
  COUNT(DISTINCT fde.customer_key) AS defaulted_customers,
  ROUND(COUNT(DISTINCT fde.customer_key)::NUMERIC / COUNT(DISTINCT fes.customer_key) * 100, 2) AS default_rate_pct,
  ROUND(SUM(fes.current_exposure), 2) AS total_exposure_eur,
  ROUND(SUM(fes.overdue_exposure), 2) AS total_overdue_exposure_eur,
  ROUND(SUM(fes.overdue_exposure) / SUM(fes.current_exposure) * 100, 2) AS portfolio_overdue_ratio_pct,
  ROUND(AVG(fes.utilization_ratio), 4) AS avg_utilization_ratio,
  ROUND(AVG(fes.avg_days_past_due), 2) AS avg_dpd,
  COUNT(DISTINCT CASE WHEN fes.warning_flag THEN fes.customer_key END) AS customers_with_warning,
  COUNT(DISTINCT CASE WHEN fes.stress_flag THEN fes.customer_key END) AS customers_under_stress
FROM credit_risk.fact_exposure_snapshot fes
LEFT JOIN credit_risk.fact_default_event fde ON fes.customer_key = fde.customer_key
  AND fes.snapshot_date >= fde.default_date
GROUP BY fes.year_month
ORDER BY fes.year_month DESC;

COMMENT ON VIEW credit_risk.vw_monthly_portfolio_kpis IS 'Portfolio-level KPIs aggregated by month';
