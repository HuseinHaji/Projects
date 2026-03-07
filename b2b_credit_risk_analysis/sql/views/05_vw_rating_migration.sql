-- View: Rating Migration Matrix
-- Tracks transitions between rating grades over time
CREATE OR REPLACE VIEW credit_risk.vw_rating_migration AS
SELECT
  frh.previous_rating_code AS from_rating,
  frh.rating_code AS to_rating,
  COUNT(*) AS transition_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY frh.previous_rating_code), 2) AS migration_pct,
  CASE 
    WHEN frh.is_upgrade THEN 'Upgrade'
    WHEN frh.is_downgrade THEN 'Downgrade'
    ELSE 'Lateral'
  END AS transition_type
FROM credit_risk.fact_rating_history frh
WHERE frh.previous_rating_code IS NOT NULL
GROUP BY frh.previous_rating_code, frh.rating_code, transition_type
ORDER BY frh.previous_rating_code, transition_count DESC;

COMMENT ON VIEW credit_risk.vw_rating_migration IS 'Rating transition matrix showing migration patterns between grades';
