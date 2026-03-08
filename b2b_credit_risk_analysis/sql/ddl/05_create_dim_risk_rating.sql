-- Dimension: Risk Rating
CREATE TABLE credit_risk_dw.dim_risk_rating (
    rating_key          INTEGER PRIMARY KEY,
    rating_code         VARCHAR(10) NOT NULL UNIQUE,
    rating_score        INTEGER NOT NULL,
    rating_bucket       VARCHAR(20) NOT NULL,
    pd_band_low         DECIMAL(8,4),
    pd_band_high        DECIMAL(8,4)
);