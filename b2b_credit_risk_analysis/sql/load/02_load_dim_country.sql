-- Load: Dimension Country
-- Maps countries from staging to dimension with reference data
INSERT INTO credit_risk.dim_country (country_code, country_name, region)
SELECT DISTINCT
  CASE 
    WHEN country = 'Germany' THEN 'DE'
    WHEN country = 'Netherlands' THEN 'NL'
    WHEN country = 'France' THEN 'FR'
    WHEN country = 'Poland' THEN 'PL'
    WHEN country = 'Italy' THEN 'IT'
    WHEN country = 'Spain' THEN 'ES'
    WHEN country = 'Belgium' THEN 'BE'
    WHEN country = 'Austria' THEN 'AT'
    ELSE UPPER(SUBSTRING(country, 1, 2))
  END,
  country,
  CASE 
    WHEN country IN ('Germany', 'Netherlands', 'France', 'Belgium', 'Austria') THEN 'Western Europe'
    WHEN country IN ('Poland', 'Italy', 'Spain') THEN 'Southern/Eastern Europe'
    ELSE 'Europe'
  END
FROM credit_risk.stg_customer
WHERE country IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM credit_risk.dim_country dc 
    WHERE dc.country_name = stg_customer.country
  );

COMMENT ON TABLE credit_risk.dim_country IS 'Countries loaded from staging customer data';
