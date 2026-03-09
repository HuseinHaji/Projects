CREATE TABLE IF NOT EXISTS credit_risk_dw.fact_invoice (
    invoice_key          BIGINT PRIMARY KEY,
    invoice_id           VARCHAR(50) NOT NULL UNIQUE,
    customer_key         INTEGER NOT NULL,
    invoice_date_key     INTEGER NOT NULL,
    due_date_key         INTEGER NOT NULL,
    invoice_amount       NUMERIC(18,2) NOT NULL,
    currency_code        VARCHAR(10) NOT NULL,
    payment_terms_days   INTEGER NOT NULL,
    product_category     VARCHAR(100),
    insured_flag         INTEGER NOT NULL,
    invoice_status       VARCHAR(30) NOT NULL,
    CONSTRAINT fk_invoice_customer
        FOREIGN KEY (customer_key) REFERENCES credit_risk_dw.dim_customer(customer_key),
    CONSTRAINT fk_invoice_invoice_date
        FOREIGN KEY (invoice_date_key) REFERENCES credit_risk_dw.dim_date(date_key),
    CONSTRAINT fk_invoice_due_date
        FOREIGN KEY (due_date_key) REFERENCES credit_risk_dw.dim_date(date_key)
);