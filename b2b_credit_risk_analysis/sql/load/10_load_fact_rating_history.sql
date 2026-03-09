TRUNCATE TABLE credit_risk_dw.fact_rating_history RESTART IDENTITY CASCADE;

COPY credit_risk_dw.fact_rating_history (
    rating_history_key,
    customer_key,
    snapshot_date_key,
    rating_key,
    rating_score,
    notch_change,
    downgrade_flag
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/fact_rating_history.csv'
DELIMITER ','
CSV HEADER;