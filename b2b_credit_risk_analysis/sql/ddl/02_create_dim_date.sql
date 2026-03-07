-- Dimension: Date
CREATE TABLE IF NOT EXISTS credit_risk.dim_date (
  date_key SERIAL PRIMARY KEY,
  date_id DATE UNIQUE NOT NULL,
  year SMALLINT NOT NULL,
  quarter SMALLINT NOT NULL,
  month SMALLINT NOT NULL,
  day SMALLINT NOT NULL,
  day_of_week SMALLINT NOT NULL,
  day_name VARCHAR(10) NOT NULL,
  month_name VARCHAR(20) NOT NULL,
  is_weekend BOOLEAN NOT NULL,
  is_month_end BOOLEAN NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dim_date_date_id ON credit_risk.dim_date(date_id);
COMMENT ON TABLE credit_risk.dim_date IS 'Date dimension for time-based analysis';
