-- Load: Fact Default Event
-- Loads default events from staging
INSERT INTO credit_risk.fact_default_event (
  default_event_key, customer_key, default_date_key, default_date,
  default_amount, recovery_amount, net_loss_amount, default_reason,
  claim_status, days_from_first_overdue
)
SELECT
  sde.default_event_key,
  sde.customer_key,
  dd.date_key,
  sde.default_date,
  sde.default_amount,
  sde.recovery_amount,
  sde.net_loss_amount,
  sde.default_reason,
  sde.claim_status,
  sde.days_from_first_overdue
FROM credit_risk.stg_default_event sde
LEFT JOIN credit_risk.dim_date dd ON sde.default_date = dd.date_id
WHERE NOT EXISTS (
  SELECT 1 FROM credit_risk.fact_default_event fde 
  WHERE fde.default_event_key = sde.default_event_key
);

COMMENT ON TABLE credit_risk.fact_default_event IS 'Default events loaded from staging';
