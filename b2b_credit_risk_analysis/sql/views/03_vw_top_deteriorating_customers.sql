-- View: Top Deteriorating Customers
-- Identifies customers with the worst rating changes and increased risk
CREATE OR REPLACE VIEW credit_risk.vw_top_deteriorating_customers AS
WITH latest_snapshot AS (
  SELECT
    customer_key,
    snapshot_date,
    rating_code,
    rating_score,
    current_exposure,
    utilization_ratio,
    avg_days_past_due,
    ROW_NUMBER() OVER (PARTITION BY customer_key ORDER BY snapshot_date DESC) AS rn
  FROM credit_risk.fact_exposure_snapshot
),
previous_snapshot AS (
  SELECT
    customer_key,
    snapshot_date,
    rating_code,
    rating_score,
    ROW_NUMBER() OVER (PARTITION BY customer_key ORDER BY snapshot_date DESC) AS rn
  FROM credit_risk.fact_exposure_snapshot
)
SELECT
  dc.customer_id,
  dc.customer_name,
  c.country_name,
  i.industry_name,
  ls.rating_code AS current_rating,
  ps.rating_code AS previous_rating,
  (ps.rating_score - ls.rating_score)::SMALLINT AS rating_deterioration_notches,
  ls.current_exposure,
  ls.utilization_ratio,
  ls.avg_days_past_due,
  ls.snapshot_date AS last_snapshot_date
FROM latest_snapshot ls
LEFT JOIN previous_snapshot ps ON ls.customer_key = ps.customer_key AND ps.rn = 2
LEFT JOIN credit_risk.dim_customer dc ON ls.customer_key = dc.customer_key
LEFT JOIN credit_risk.dim_country c ON dc.country_key = c.country_key
LEFT JOIN credit_risk.dim_industry i ON dc.industry_key = i.industry_key
WHERE ls.rn = 1 AND (ps.rating_score - ls.rating_score) > 0
ORDER BY rating_deterioration_notches DESC
LIMIT 50;

COMMENT ON VIEW credit_risk.vw_top_deteriorating_customers IS 'Top 50 customers with worst rating deterioration';
