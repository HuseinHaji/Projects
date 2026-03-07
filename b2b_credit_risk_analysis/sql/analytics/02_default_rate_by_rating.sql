-- Analytics: Default Rate by Rating Grade
-- PD (Probability of Default) analysis by credit rating
SELECT
  drr.rating_code,
  drr.rating_category,
  COUNT(DISTINCT fes.customer_key) AS customers_in_grade,
  COUNT(DISTINCT CASE WHEN fde.default_event_key IS NOT NULL THEN fes.customer_key END) AS defaults,
  ROUND(
    100.0 * COUNT(DISTINCT CASE WHEN fde.default_event_key IS NOT NULL THEN fes.customer_key END) /
    COUNT(DISTINCT fes.customer_key),
    3
  ) AS pd_pct,
  ROUND(SUM(fes.current_exposure), 2) AS total_exposure_eur,
  ROUND(SUM(CASE WHEN fde.default_event_key IS NOT NULL THEN fde.net_loss_amount ELSE 0 END), 2) AS realized_losses_eur
FROM credit_risk.fact_exposure_snapshot fes
LEFT JOIN credit_risk.dim_risk_rating drr ON fes.rating_code = drr.rating_code
LEFT JOIN credit_risk.fact_default_event fde ON fes.customer_key = fde.customer_key
GROUP BY drr.rating_code, drr.rating_category
ORDER BY drr.rating_score;
