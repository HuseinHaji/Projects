TRUNCATE TABLE credit_risk_dw.dim_risk_rating RESTART IDENTITY CASCADE;

COPY credit_risk_dw.dim_risk_rating (
    rating_key,
    rating_code,
    rating_score,
    rating_bucket,
    pd_band_low,
    pd_band_high
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/dim_risk_rating.csv'
DELIMITER ','
CSV HEADER;