CREATE TABLE IF NOT EXISTS credit_risk_dw.dim_country (
    country_key         INTEGER PRIMARY KEY,
    country_name        VARCHAR(100) NOT NULL UNIQUE,
    country_code        VARCHAR(10) NOT NULL,
    region_name         VARCHAR(100),
    risk_region         VARCHAR(20),
    eur_currency_flag   INTEGER NOT NULL
);