TRUNCATE TABLE credit_risk_dw.dim_date RESTART IDENTITY CASCADE;

COPY credit_risk_dw.dim_date (
    date_key,
    full_date,
    year_num,
    quarter_num,
    month_num,
    month_name,
    year_month,
    week_of_year,
    day_of_month,
    day_name,
    is_month_start,
    is_month_end,
    is_quarter_end,
    is_year_end
)
FROM '/ABSOLUTE/PATH/TO/data/processed/phase2/dim_date.csv'
DELIMITER ','
CSV HEADER;