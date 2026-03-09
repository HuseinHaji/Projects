CREATE TABLE IF NOT EXISTS credit_risk_dw.fact_exposure_snapshot (
    exposure_snapshot_key    BIGINT PRIMARY KEY,
    customer_key             INTEGER NOT NULL,
    snapshot_date_key        INTEGER NOT NULL,
    rating_key               INTEGER NOT NULL,
    monthly_sales_estimate   NUMERIC(18,2),
    invoice_count_month      INTEGER,
    current_exposure         NUMERIC(18,2) NOT NULL,
    overdue_exposure         NUMERIC(18,2) NOT NULL,
    overdue_ratio            NUMERIC(10,4) NOT NULL,
    insured_limit            NUMERIC(18,2) NOT NULL,
    utilization_ratio        NUMERIC(10,4) NOT NULL,
    avg_days_past_due        NUMERIC(10,2),
    max_days_past_due        INTEGER,
    open_invoice_count       INTEGER,
    notch_change             INTEGER,
    downgrade_flag           INTEGER NOT NULL,
    stress_flag              INTEGER NOT NULL,
    warning_flag             INTEGER NOT NULL,
    default_in_next_90d      INTEGER NOT NULL,
    is_defaulted             INTEGER NOT NULL,
    CONSTRAINT fk_exp_customer
        FOREIGN KEY (customer_key) REFERENCES credit_risk_dw.dim_customer(customer_key),
    CONSTRAINT fk_exp_snapshot_date
        FOREIGN KEY (snapshot_date_key) REFERENCES credit_risk_dw.dim_date(date_key),
    CONSTRAINT fk_exp_rating
        FOREIGN KEY (rating_key) REFERENCES credit_risk_dw.dim_risk_rating(rating_key)
);