WITH monthly AS (
    SELECT
        dd.year_month,
        SUM(f.overdue_exposure) AS overdue_exp,
        SUM(f.current_exposure) AS total_exp
    FROM credit_risk_dw.fact_exposure_snapshot f
    JOIN credit_risk_dw.dim_date dd
        ON f.snapshot_date_key = dd.date_key
    GROUP BY dd.year_month
)
SELECT
    year_month,
    overdue_exp,
    total_exp,
    CASE
        WHEN total_exp = 0 THEN 0
        ELSE overdue_exp / total_exp
    END AS overdue_rate,
    AVG(
        CASE
            WHEN total_exp = 0 THEN 0
            ELSE overdue_exp / total_exp
        END
    ) OVER (
        ORDER BY year_month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS overdue_rate_3m_rolling
FROM monthly
ORDER BY year_month;