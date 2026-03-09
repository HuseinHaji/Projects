import numpy as np
import pandas as pd

def generate_payments(invoices_with_context, seed=42):
    rng = np.random.default_rng(seed)
    payment_rows = []
    payment_key = 1

    for row in invoices_with_context.itertuples(index=False):
        latent = 0.0 if pd.isna(row.latent_state) else row.latent_state
        avg_dpd = 0.0 if pd.isna(row.avg_days_past_due) else row.avg_days_past_due
        overdue_ratio = 0.0 if pd.isna(row.overdue_ratio) else row.overdue_ratio
        util = 0.4 if pd.isna(row.utilization_ratio) else row.utilization_ratio
        rating_score = 4 if pd.isna(row.rating_score) else row.rating_score
        stress_flag = 0 if pd.isna(row.stress_flag) else row.stress_flag

        payment_stress = (
            0.7 * max(latent, 0)
            + 0.02 * avg_dpd
            + 1.1 * overdue_ratio
            + 0.7 * max(util - 0.8, 0)
            + 0.18 * (rating_score - 4)
            + 0.35 * stress_flag
        )

        if payment_stress < 0.35:
            probs = [0.82, 0.14, 0.03, 0.01]   # on-time, late-full, partial, unpaid
        elif payment_stress < 0.90:
            probs = [0.55, 0.28, 0.10, 0.07]
        else:
            probs = [0.22, 0.33, 0.20, 0.25]

        outcome = rng.choice(["on_time", "late_full", "partial", "unpaid"], p=probs)

        if outcome == "on_time":
            days_late = int(max(0, rng.normal(0, 2)))
            payment_amount = row.invoice_amount
            payment_status = "Paid"
            partial_payment_flag = 0
            recovered_after_default_flag = 0
            payment_date = pd.Timestamp(row.due_date) + pd.Timedelta(days=days_late)

            payment_rows.append({
                "payment_key": payment_key,
                "invoice_key": row.invoice_key,
                "payment_date": payment_date.normalize(),
                "payment_amount": round(float(payment_amount), 2),
                "days_late": days_late,
                "partial_payment_flag": partial_payment_flag,
                "payment_status": payment_status,
                "recovered_after_default_flag": recovered_after_default_flag,
            })
            payment_key += 1

        elif outcome == "late_full":
            days_late = int(np.clip(rng.gamma(2.2, 12), 3, 140))
            payment_amount = row.invoice_amount
            payment_status = "Paid"
            partial_payment_flag = 0
            recovered_after_default_flag = 0
            payment_date = pd.Timestamp(row.due_date) + pd.Timedelta(days=days_late)

            payment_rows.append({
                "payment_key": payment_key,
                "invoice_key": row.invoice_key,
                "payment_date": payment_date.normalize(),
                "payment_amount": round(float(payment_amount), 2),
                "days_late": days_late,
                "partial_payment_flag": partial_payment_flag,
                "payment_status": payment_status,
                "recovered_after_default_flag": recovered_after_default_flag,
            })
            payment_key += 1

        elif outcome == "partial":
            days_late = int(np.clip(rng.gamma(2.0, 15), 5, 180))
            pay_frac = rng.uniform(0.30, 0.80)
            payment_amount = row.invoice_amount * pay_frac
            payment_status = "Partial"
            partial_payment_flag = 1
            recovered_after_default_flag = 0
            payment_date = pd.Timestamp(row.due_date) + pd.Timedelta(days=days_late)

            payment_rows.append({
                "payment_key": payment_key,
                "invoice_key": row.invoice_key,
                "payment_date": payment_date.normalize(),
                "payment_amount": round(float(payment_amount), 2),
                "days_late": days_late,
                "partial_payment_flag": partial_payment_flag,
                "payment_status": payment_status,
                "recovered_after_default_flag": recovered_after_default_flag,
            })
            payment_key += 1

        else:
            # unpaid invoices produce no payment row in first version
            pass

    return pd.DataFrame(payment_rows)