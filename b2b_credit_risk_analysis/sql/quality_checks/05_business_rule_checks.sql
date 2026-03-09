SELECT COUNT(*) AS invalid_overdue_rows
FROM credit_risk_dw.fact_exposure_snapshot
WHERE overdue_exposure > current_exposure;

SELECT COUNT(*) AS invalid_overdue_ratio_rows
FROM credit_risk_dw.fact_exposure_snapshot
WHERE overdue_ratio < 0 OR overdue_ratio > 1;

SELECT COUNT(*) AS invalid_utilization_rows
FROM credit_risk_dw.fact_exposure_snapshot
WHERE utilization_ratio < 0;

SELECT COUNT(*) AS invalid_recovery_rows
FROM credit_risk_dw.fact_default_event
WHERE recovery_amount > default_amount;

SELECT COUNT(*) AS invalid_net_loss_rows
FROM credit_risk_dw.fact_default_event
WHERE ROUND(net_loss_amount, 2) <> ROUND(default_amount - recovery_amount, 2);

SELECT COUNT(*) AS invalid_invoice_date_order
FROM credit_risk_dw.fact_invoice
WHERE due_date_key < invoice_date_key;

SELECT COUNT(*) AS invalid_negative_payment_amount
FROM credit_risk_dw.fact_payment
WHERE payment_amount <= 0;

SELECT COUNT(*) AS invalid_negative_invoice_amount
FROM credit_risk_dw.fact_invoice
WHERE invoice_amount <= 0;