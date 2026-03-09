SELECT
    dd.year_num,
    dd.month_num,
    dd.year_month,
    SUM(f.current_exposure) AS total_exposure,
    SUM(f.overdue_exposure) AS total_overdue_exposure,
    CASE
        WHEN SUM(f.current_exposure) = 0 THEN 0
        ELSE SUM(f.overdue_exposure) / SUM(f.current_exposure)
    END AS overdue_rate,
    AVG(f.utilization_ratio) AS avg_utilization_ratio,
    COUNT(DISTINCT f.customer_key) AS active_customers
FROM credit_risk_dw.fact_exposure_snapshot f
JOIN credit_risk_dw.dim_date dd
    ON f.snapshot_date_key = dd.date_key
GROUP BY dd.year_num, dd.month_num, dd.year_month
ORDER BY dd.year_num, dd.month_num;