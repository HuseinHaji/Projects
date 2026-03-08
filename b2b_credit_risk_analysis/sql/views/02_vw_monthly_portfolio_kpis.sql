-- View: Monthly Portfolio KPIs
-- Aggregated portfolio metrics by month
CREATE OR REPLACE VIEW credit_risk_dw.vw_monthly_portfolio_kpis AS
SELECT
    dd.year_month,
    SUM(fes.current_exposure) AS total_exposure,
    SUM(fes.overdue_exposure) AS overdue_exposure,
    CASE
        WHEN SUM(fes.current_exposure) = 0 THEN 0
        ELSE SUM(fes.overdue_exposure) / SUM(fes.current_exposure)
    END AS overdue_rate,
    AVG(fes.utilization_ratio) AS avg_utilization_ratio,
    AVG(fes.avg_days_past_due) AS avg_days_past_due,
    SUM(fes.warning_flag) AS warning_flag_count,
    SUM(fes.default_in_next_90d) AS default_target_count
FROM credit_risk_dw.fact_exposure_snapshot fes
JOIN credit_risk_dw.dim_date dd
    ON fes.snapshot_date_key = dd.date_key
GROUP BY dd.year_month;
