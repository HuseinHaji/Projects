CREATE TABLE IF NOT EXISTS credit_risk_dw.fact_rating_history (
    rating_history_key    BIGINT PRIMARY KEY,
    customer_key          INTEGER NOT NULL,
    snapshot_date_key     INTEGER NOT NULL,
    rating_key            INTEGER NOT NULL,
    rating_score          INTEGER NOT NULL,
    notch_change          INTEGER,
    downgrade_flag        INTEGER NOT NULL,
    CONSTRAINT fk_rating_hist_customer
        FOREIGN KEY (customer_key) REFERENCES credit_risk_dw.dim_customer(customer_key),
    CONSTRAINT fk_rating_hist_date
        FOREIGN KEY (snapshot_date_key) REFERENCES credit_risk_dw.dim_date(date_key),
    CONSTRAINT fk_rating_hist_rating
        FOREIGN KEY (rating_key) REFERENCES credit_risk_dw.dim_risk_rating(rating_key)
);