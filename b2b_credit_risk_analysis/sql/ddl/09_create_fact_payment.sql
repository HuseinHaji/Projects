CREATE TABLE IF NOT EXISTS credit_risk_dw.fact_payment (
    payment_key                   BIGINT PRIMARY KEY,
    invoice_key                   BIGINT NOT NULL,
    payment_date_key              INTEGER NOT NULL,
    payment_amount                NUMERIC(18,2) NOT NULL,
    days_late                     INTEGER NOT NULL,
    partial_payment_flag          INTEGER NOT NULL,
    payment_status                VARCHAR(30) NOT NULL,
    recovered_after_default_flag  INTEGER NOT NULL,
    CONSTRAINT fk_payment_invoice
        FOREIGN KEY (invoice_key) REFERENCES credit_risk_dw.fact_invoice(invoice_key),
    CONSTRAINT fk_payment_date
        FOREIGN KEY (payment_date_key) REFERENCES credit_risk_dw.dim_date(date_key)
);