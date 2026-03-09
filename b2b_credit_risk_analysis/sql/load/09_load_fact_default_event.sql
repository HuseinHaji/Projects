TRUNCATE TABLE credit_risk_dw.fact_default_event RESTART IDENTITY CASCADE;

COPY credit_risk_dw.fact_default_event (
    default_event_key,
    customer_key,
    default_date_key,
    default_amount,
    recovery_amount,
    net_loss_amount,
    default_reason,
    claim_status,
    days_from_first_overdue
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/fact_default_event.csv'
DELIMITER ','
CSV HEADER;