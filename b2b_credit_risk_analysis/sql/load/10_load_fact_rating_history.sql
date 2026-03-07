-- Load: Fact Rating History
-- Constructs rating history from exposure snapshot changes
INSERT INTO credit_risk.fact_rating_history (
  rating_history_key, customer_key, rating_key, date_key, rating_date,
  rating_code, rating_score, previous_rating_code, previous_rating_score,
  notch_change, is_downgrade, is_upgrade
)
WITH rating_changes AS (
  SELECT
    ROW_NUMBER() OVER (ORDER BY customer_key, snapshot_date),
    fes.customer_key,
    fes.date_key,
    fes.snapshot_date,
    fes.rating_code,
    fes.rating_score,
    LAG(fes.rating_code) OVER (PARTITION BY fes.customer_key ORDER BY fes.snapshot_date) AS prev_rating_code,
    LAG(fes.rating_score) OVER (PARTITION BY fes.customer_key ORDER BY fes.snapshot_date) AS prev_rating_score,
    fes.notch_change
  FROM credit_risk.fact_exposure_snapshot fes
  WHERE fes.rating_code IS NOT NULL
)
SELECT
  rc.row_number,
  rc.customer_key,
  drr.rating_key,
  rc.date_key,
  rc.snapshot_date,
  rc.rating_code,
  rc.rating_score,
  rc.prev_rating_code,
  rc.prev_rating_score,
  rc.notch_change,
  rc.notch_change > 0,
  rc.notch_change < 0
FROM rating_changes rc
LEFT JOIN credit_risk.dim_risk_rating drr ON rc.rating_code = drr.rating_code
WHERE rc.prev_rating_code IS NOT NULL
  AND rc.prev_rating_code != rc.rating_code
  AND NOT EXISTS (
    SELECT 1 FROM credit_risk.fact_rating_history frh 
    WHERE frh.customer_key = rc.customer_key 
      AND frh.rating_date = rc.snapshot_date
  );

COMMENT ON TABLE credit_risk.fact_rating_history IS 'Rating migration history constructed from snapshot deltas';
