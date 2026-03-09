SELECT
    rr.rating_code,
    rr.rating_score,
    AVG(f.default_in_next_90d::numeric) AS default_rate_next_90d,
    COUNT(*) AS observation_count
FROM credit_risk_dw.fact_exposure_snapshot f
JOIN credit_risk_dw.dim_risk_rating rr
    ON f.rating_key = rr.rating_key
GROUP BY rr.rating_code, rr.rating_score
ORDER BY rr.rating_score;