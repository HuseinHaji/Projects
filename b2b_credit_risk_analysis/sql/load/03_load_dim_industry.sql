TRUNCATE TABLE credit_risk_dw.dim_industry RESTART IDENTITY CASCADE;

COPY credit_risk_dw.dim_industry (
    industry_key,
    industry_name,
    industry_code,
    industry_risk_level,
    cyclical_flag
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/dim_industry.csv'
DELIMITER ','
CSV HEADER;