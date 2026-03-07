-- Load: Dimension Risk Rating
-- Populates risk rating dimension with standard rating scale
INSERT INTO credit_risk.dim_risk_rating (rating_code, rating_score, rating_category, risk_tier)
VALUES
  ('AAA', 1, 'Investment Grade', 'Excellent'),
  ('AA', 2, 'Investment Grade', 'Very Good'),
  ('A', 3, 'Investment Grade', 'Good'),
  ('BBB', 4, 'Investment Grade', 'Acceptable'),
  ('BB', 5, 'Speculative', 'Risky'),
  ('B', 6, 'Speculative', 'Very Risky'),
  ('CCC', 7, 'Speculative', 'Extreme Risk')
ON CONFLICT (rating_code) DO NOTHING;

COMMENT ON TABLE credit_risk.dim_risk_rating IS 'Standard risk rating scale with 7 notches';
