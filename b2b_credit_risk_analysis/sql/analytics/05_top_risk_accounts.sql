SELECT
    dc.customer_id,
    dc.customer_name,
    co.country_name,
    di.industry_name,
    dd.full_date AS snapshot_date,
    rr.rating_code,
    f.current_exposure,
    f.overdue_exposure,
    f.overdue_ratio,
    f.utilization_ratio,
    f.avg_days_past_due,
    f.max_days_past_due,
    f.notch_change,
    f.downgrade_flag,
    f.warning_flag,
    f.default_in_next_90d
FROM credit_risk_dw.fact_exposure_snapshot f
JOIN credit_risk_dw.dim_customer dc
    ON f.customer_key = dc.customer_key
JOIN credit_risk_dw.dim_country co
    ON dc.country_key = co.country_key
JOIN credit_risk_dw.dim_industry di
    ON dc.industry_key = di.industry_key
JOIN credit_risk_dw.dim_date dd
    ON f.snapshot_date_key = dd.date_key
JOIN credit_risk_dw.dim_risk_rating rr
    ON f.rating_key = rr.rating_key
WHERE
    f.warning_flag = 1
    OR f.downgrade_flag = 1
    OR f.default_in_next_90d = 1
ORDER BY
    f.overdue_exposure DESC,
    f.avg_days_past_due DESC,
    f.utilization_ratio DESC;