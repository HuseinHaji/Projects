-- Load: Dimension Date
-- Generates and loads a complete date dimension for the analysis period
INSERT INTO credit_risk.dim_date (date_id, year, quarter, month, day, day_of_week, day_name, month_name, is_weekend, is_month_end)
WITH RECURSIVE date_series AS (
  SELECT '2022-01-01'::DATE AS date_id
  UNION ALL
  SELECT date_id + INTERVAL '1 day'
  FROM date_series
  WHERE date_id < '2025-12-31'::DATE
)
SELECT
  date_id,
  EXTRACT(YEAR FROM date_id)::SMALLINT,
  EXTRACT(QUARTER FROM date_id)::SMALLINT,
  EXTRACT(MONTH FROM date_id)::SMALLINT,
  EXTRACT(DAY FROM date_id)::SMALLINT,
  EXTRACT(DOW FROM date_id)::SMALLINT,
  TO_CHAR(date_id, 'Day'),
  TO_CHAR(date_id, 'Month'),
  EXTRACT(DOW FROM date_id) IN (0, 6),
  (date_id + INTERVAL '1 day')::DATE = DATE_TRUNC('MONTH', date_id + INTERVAL '1 MONTH')::DATE
FROM date_series
WHERE NOT EXISTS (SELECT 1 FROM credit_risk.dim_date WHERE date_id = date_series.date_id)
ORDER BY date_id;

COMMENT ON COLUMN credit_risk.dim_date.date_id IS 'Date value for joining';
