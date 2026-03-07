-- Load: Dimension Industry
-- Maps industries from staging to dimension with reference data
INSERT INTO credit_risk.dim_industry (industry_code, industry_name, sector)
SELECT DISTINCT
  UPPER(SUBSTRING(industry, 1, 3)),
  industry,
  CASE 
    WHEN industry = 'Manufacturing' THEN 'Primary'
    WHEN industry IN ('Wholesale', 'Retail', 'Logistics') THEN 'Distribution'
    WHEN industry IN ('Construction', 'Pharma', 'Food & Beverage', 'Electronics') THEN 'Manufacturing'
    ELSE 'Services'
  END
FROM credit_risk.stg_customer
WHERE industry IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM credit_risk.dim_industry di 
    WHERE di.industry_name = stg_customer.industry
  );

COMMENT ON TABLE credit_risk.dim_industry IS 'Industries loaded from staging customer data';
