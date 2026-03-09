SELECT
    co.country_name,
    di.industry_name,
    SUM(f.current_exposure) AS total_exposure,
    SUM(f.overdue_exposure) AS total_overdue_exposure,
    AVG(f.utilization_ratio) AS avg_utilization_ratio,
    AVG(f.avg_days_past_due) AS avg_days_past_due
FROM credit_risk_dw.fact_exposure_snapshot f
JOIN credit_risk_dw.dim_customer dc
    ON f.customer_key = dc.customer_key
JOIN credit_risk_dw.dim_country co
    ON dc.country_key = co.country_key
JOIN credit_risk_dw.dim_industry di
    ON dc.industry_key = di.industry_key
GROUP BY co.country_name, di.industry_name
ORDER BY total_exposure DESC;