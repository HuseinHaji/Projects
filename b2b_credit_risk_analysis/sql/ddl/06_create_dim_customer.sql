CREATE TABLE IF NOT EXISTS credit_risk_dw.dim_customer (
    customer_key            INTEGER PRIMARY KEY,
    customer_id             VARCHAR(50) NOT NULL UNIQUE,
    customer_name           VARCHAR(200) NOT NULL,
    country_key             INTEGER NOT NULL,
    industry_key            INTEGER NOT NULL,
    company_size            VARCHAR(20) NOT NULL,
    years_in_business       INTEGER NOT NULL,
    annual_revenue_eur      NUMERIC(18,2) NOT NULL,
    employee_count          INTEGER NOT NULL,
    onboarding_date_key     INTEGER NOT NULL,
    legal_form              VARCHAR(50),
    parent_group_flag       INTEGER NOT NULL,
    base_risk_score         NUMERIC(12,6),
    base_insured_limit      NUMERIC(18,2),
    active_flag             INTEGER NOT NULL,
    CONSTRAINT fk_dim_customer_country
        FOREIGN KEY (country_key) REFERENCES credit_risk_dw.dim_country(country_key),
    CONSTRAINT fk_dim_customer_industry
        FOREIGN KEY (industry_key) REFERENCES credit_risk_dw.dim_industry(industry_key),
    CONSTRAINT fk_dim_customer_onboard_date
        FOREIGN KEY (onboarding_date_key) REFERENCES credit_risk_dw.dim_date(date_key)
);