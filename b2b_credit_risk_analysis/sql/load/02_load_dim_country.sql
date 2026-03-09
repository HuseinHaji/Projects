TRUNCATE TABLE credit_risk_dw.dim_country RESTART IDENTITY CASCADE;

COPY credit_risk_dw.dim_country (
    country_key,
    country_name,
    country_code,
    region_name,
    risk_region,
    eur_currency_flag
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/dim_country.csv'
DELIMITER ','
CSV HEADER;