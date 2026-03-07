-- Load: Dimension Customer
-- Loads customer master dimension from staging with lookups
INSERT INTO credit_risk.dim_customer (
  customer_key, customer_id, customer_name, country_key, industry_key,
  company_size, years_in_business, annual_revenue_eur, employee_count,
  legal_form, parent_group_flag, base_risk_score, base_insured_limit,
  onboarding_date, active_flag
)
SELECT
  sc.customer_key,
  sc.customer_id,
  sc.customer_name,
  dc.country_key,
  di.industry_key,
  sc.company_size,
  sc.years_in_business,
  sc.annual_revenue_eur,
  sc.employee_count,
  sc.legal_form,
  sc.parent_group_flag,
  sc.base_risk_score,
  sc.base_insured_limit,
  sc.onboarding_date,
  sc.active_flag
FROM credit_risk.stg_customer sc
LEFT JOIN credit_risk.dim_country dc ON sc.country = dc.country_name
LEFT JOIN credit_risk.dim_industry di ON sc.industry = di.industry_name
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.dim_customer dc2 
  WHERE dc2.customer_key = sc.customer_key
);

COMMENT ON TABLE credit_risk.dim_customer IS 'Customer master loaded from staging with dimension lookups';
