TRUNCATE TABLE credit_risk_dw.dim_customer RESTART IDENTITY CASCADE;

COPY credit_risk_dw.dim_customer (
    customer_key,
    customer_id,
    customer_name,
    country_key,
    industry_key,
    company_size,
    years_in_business,
    annual_revenue_eur,
    employee_count,
    onboarding_date_key,
    legal_form,
    parent_group_flag,
    base_risk_score,
    base_insured_limit,
    active_flag
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/dim_customer.csv'
DELIMITER ','
CSV HEADER;