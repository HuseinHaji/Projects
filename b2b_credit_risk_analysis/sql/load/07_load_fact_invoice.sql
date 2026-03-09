TRUNCATE TABLE credit_risk_dw.fact_invoice RESTART IDENTITY CASCADE;

COPY credit_risk_dw.fact_invoice (
    invoice_key,
    invoice_id,
    customer_key,
    invoice_date_key,
    due_date_key,
    invoice_amount,
    currency_code,
    payment_terms_days,
    product_category,
    insured_flag,
    invoice_status
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/fact_invoice.csv'
DELIMITER ','
CSV HEADER;