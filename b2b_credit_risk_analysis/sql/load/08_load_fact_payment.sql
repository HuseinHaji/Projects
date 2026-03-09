TRUNCATE TABLE credit_risk_dw.fact_payment RESTART IDENTITY CASCADE;

COPY credit_risk_dw.fact_payment (
    payment_key,
    invoice_key,
    payment_date_key,
    payment_amount,
    days_late,
    partial_payment_flag,
    payment_status,
    recovered_after_default_flag
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/fact_payment.csv'
DELIMITER ','
CSV HEADER;