CREATE OR REPLACE VIEW credit_risk_dw.vw_top_deteriorating_customers AS
WITH base AS (
    SELECT
        fes.customer_key,
        dd.full_date AS snapshot_date,
        fes.current_exposure,
        fes.overdue_exposure,
        fes.utilization_ratio,
        fes.avg_days_past_due,
        fes.notch_change,
        fes.downgrade_flag,
        LAG(fes.avg_days_past_due) OVER (
            PARTITION BY fes.customer_key
            ORDER BY dd.full_date
        ) AS prev_avg_dpd,
        LAG(fes.utilization_ratio) OVER (
            PARTITION BY fes.customer_key
            ORDER BY dd.full_date
        ) AS prev_utilization
    FROM credit_risk_dw.fact_exposure_snapshot fes
    JOIN credit_risk_dw.dim_date dd
        ON fes.snapshot_date_key = dd.date_key
)
SELECT
    customer_key,
    snapshot_date,
    current_exposure,
    overdue_exposure,
    utilization_ratio,
    avg_days_past_due,
    notch_change,
    downgrade_flag,
    avg_days_past_due - COALESCE(prev_avg_dpd, avg_days_past_due) AS dpd_delta,
    utilization_ratio - COALESCE(prev_utilization, utilization_ratio) AS util_delta
FROM base
WHERE
    downgrade_flag = 1
    OR avg_days_past_due - COALESCE(prev_avg_dpd, 0) > 10
    OR utilization_ratio - COALESCE(prev_utilization, 0) > 0.10;