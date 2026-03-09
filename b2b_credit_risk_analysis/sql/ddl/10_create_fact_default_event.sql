CREATE TABLE IF NOT EXISTS credit_risk_dw.fact_default_event (
    default_event_key         BIGINT PRIMARY KEY,
    customer_key              INTEGER NOT NULL,
    default_date_key          INTEGER NOT NULL,
    default_amount            NUMERIC(18,2) NOT NULL,
    recovery_amount           NUMERIC(18,2) NOT NULL,
    net_loss_amount           NUMERIC(18,2) NOT NULL,
    default_reason            VARCHAR(50),
    claim_status              VARCHAR(30),
    days_from_first_overdue   INTEGER,
    CONSTRAINT fk_default_customer
        FOREIGN KEY (customer_key) REFERENCES credit_risk_dw.dim_customer(customer_key),
    CONSTRAINT fk_default_date
        FOREIGN KEY (default_date_key) REFERENCES credit_risk_dw.dim_date(date_key)
);