CREATE OR REPLACE VIEW credit_risk_dw.vw_country_industry_loss AS
WITH exposure_base AS (
    SELECT
        dc.country_key,
        dc.industry_key,
        SUM(fes.current_exposure) AS total_exposure,
        SUM(fes.overdue_exposure) AS total_overdue_exposure
    FROM credit_risk_dw.fact_exposure_snapshot fes
    JOIN credit_risk_dw.dim_customer dc
        ON fes.customer_key = dc.customer_key
    GROUP BY dc.country_key, dc.industry_key
),
loss_base AS (
    SELECT
        dc.country_key,
        dc.industry_key,
        COUNT(*) AS default_event_count,
        SUM(fde.default_amount) AS gross_default_amount,
        SUM(fde.recovery_amount) AS recovery_amount,
        SUM(fde.net_loss_amount) AS net_loss_amount
    FROM credit_risk_dw.fact_default_event fde
    JOIN credit_risk_dw.dim_customer dc
        ON fde.customer_key = dc.customer_key
    GROUP BY dc.country_key, dc.industry_key
)
SELECT
    co.country_name,
    di.industry_name,
    COALESCE(e.total_exposure, 0) AS total_exposure,
    COALESCE(e.total_overdue_exposure, 0) AS total_overdue_exposure,
    COALESCE(l.default_event_count, 0) AS default_event_count,
    COALESCE(l.gross_default_amount, 0) AS gross_default_amount,
    COALESCE(l.recovery_amount, 0) AS recovery_amount,
    COALESCE(l.net_loss_amount, 0) AS net_loss_amount,
    CASE
        WHEN COALESCE(e.total_exposure, 0) = 0 THEN 0
        ELSE COALESCE(l.net_loss_amount, 0) / e.total_exposure
    END AS loss_rate
FROM credit_risk_dw.dim_country co
CROSS JOIN credit_risk_dw.dim_industry di
LEFT JOIN exposure_base e
    ON co.country_key = e.country_key
   AND di.industry_key = e.industry_key
LEFT JOIN loss_base l
    ON co.country_key = l.country_key
   AND di.industry_key = l.industry_key;