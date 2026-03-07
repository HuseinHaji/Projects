-- View: Loss by Country and Industry
-- Aggregates default losses by geographic and sector dimensions
CREATE OR REPLACE VIEW credit_risk.vw_country_industry_loss AS
SELECT
  c.country_name,
  i.industry_name,
  COUNT(*) AS default_count,
  ROUND(SUM(fde.default_amount), 2) AS total_gross_loss_eur,
  ROUND(SUM(fde.recovery_amount), 2) AS total_recovery_eur,
  ROUND(SUM(fde.net_loss_amount), 2) AS total_net_loss_eur,
  ROUND(SUM(fde.recovery_amount) / SUM(fde.default_amount) * 100, 2) AS recovery_rate_pct,
  COUNT(*) FILTER (WHERE fde.default_reason = 'Insolvency') AS insolvency_count,
  COUNT(*) FILTER (WHERE fde.default_reason = 'Protracted Default') AS protracted_default_count,
  COUNT(*) FILTER (WHERE fde.default_reason = 'Dispute') AS dispute_count
FROM credit_risk.fact_default_event fde
LEFT JOIN credit_risk.dim_customer dc ON fde.customer_key = dc.customer_key
LEFT JOIN credit_risk.dim_country c ON dc.country_key = c.country_key
LEFT JOIN credit_risk.dim_industry i ON dc.industry_key = i.industry_key
GROUP BY c.country_name, i.industry_name
ORDER BY total_net_loss_eur DESC;

COMMENT ON VIEW credit_risk.vw_country_industry_loss IS 'Aggregate loss metrics by country and industry';
