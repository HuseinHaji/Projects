CREATE TABLE IF NOT EXISTS credit_risk_dw.dim_industry (
    industry_key            INTEGER PRIMARY KEY,
    industry_name           VARCHAR(100) NOT NULL UNIQUE,
    industry_code           VARCHAR(20) NOT NULL,
    industry_risk_level     VARCHAR(20) NOT NULL,
    cyclical_flag           INTEGER NOT NULL
);