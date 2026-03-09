CREATE TABLE IF NOT EXISTS credit_risk_dw.dim_date (
    date_key            INTEGER PRIMARY KEY,
    full_date           DATE NOT NULL UNIQUE,
    year_num            INTEGER NOT NULL,
    quarter_num         INTEGER NOT NULL,
    month_num           INTEGER NOT NULL,
    month_name          VARCHAR(20) NOT NULL,
    year_month          VARCHAR(7) NOT NULL,
    week_of_year        INTEGER NOT NULL,
    day_of_month        INTEGER NOT NULL,
    day_name            VARCHAR(20) NOT NULL,
    is_month_start      INTEGER NOT NULL,
    is_month_end        INTEGER NOT NULL,
    is_quarter_end      INTEGER NOT NULL,
    is_year_end         INTEGER NOT NULL
);