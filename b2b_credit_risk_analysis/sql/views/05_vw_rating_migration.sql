CREATE OR REPLACE VIEW credit_risk_dw.vw_rating_migration AS
WITH hist AS (
    SELECT
        frh.customer_key,
        dd.full_date AS snapshot_date,
        rr.rating_code,
        rr.rating_score,
        LAG(rr.rating_code) OVER (
            PARTITION BY frh.customer_key ORDER BY dd.full_date
        ) AS prev_rating_code,
        LAG(rr.rating_score) OVER (
            PARTITION BY frh.customer_key ORDER BY dd.full_date
        ) AS prev_rating_score
    FROM credit_risk_dw.fact_rating_history frh
    JOIN credit_risk_dw.dim_date dd
        ON frh.snapshot_date_key = dd.date_key
    JOIN credit_risk_dw.dim_risk_rating rr
        ON frh.rating_key = rr.rating_key
)
SELECT
    prev_rating_code,
    rating_code AS current_rating_code,
    COUNT(*) AS migration_count
FROM hist
WHERE prev_rating_code IS NOT NULL
GROUP BY prev_rating_code, rating_code
ORDER BY prev_rating_code, rating_code;