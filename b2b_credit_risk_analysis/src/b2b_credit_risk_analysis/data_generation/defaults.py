import numpy as np
import pandas as pd

def generate_default_events(customer_month_panel, seed=42):
    rng = np.random.default_rng(seed)
    panel = customer_month_panel.sort_values(["customer_key", "snapshot_date"]).copy()

    default_rows = []
    defaulted_customers = set()
    default_key = 1

    for cust_key, grp in panel.groupby("customer_key"):
        grp = grp.reset_index(drop=True)

        consec_high_dpd = 0
        first_overdue_date = None

        for i, row in grp.iterrows():
            if cust_key in defaulted_customers:
                break

            if row["avg_days_past_due"] >= 45:
                consec_high_dpd += 1
                if first_overdue_date is None:
                    first_overdue_date = row["snapshot_date"]
            else:
                consec_high_dpd = 0

            eligible = (
                (consec_high_dpd >= 2)
                or (row["rating_score"] >= 6 and row["overdue_ratio"] >= 0.20)
                or (row["utilization_ratio"] > 0.95 and row["overdue_exposure"] > 0)
                or (row["warning_flag"] == 1 and i >= 2 and grp.loc[i-2:i, "warning_flag"].sum() >= 2)
            )

            if not eligible:
                continue

            z = (
                -3.5
                + 0.03 * row["avg_days_past_due"]
                + 1.2 * row["overdue_ratio"]
                + 0.9 * row["utilization_ratio"]
                + 0.35 * (row["rating_score"] - 4)
                + 0.6 * row["stress_flag"]
            )
            p = 1 / (1 + np.exp(-z))
            p = float(np.clip(p, 0.01, 0.35))

            if rng.random() < p:
                gross_amount = row["current_exposure"] * rng.uniform(0.45, 1.00)
                reason = rng.choice(
                    ["Insolvency", "Protracted Default", "Dispute"],
                    p=[0.50, 0.35, 0.15]
                )

                if reason == "Insolvency":
                    rec_frac = rng.uniform(0.05, 0.20)
                elif reason == "Protracted Default":
                    rec_frac = rng.uniform(0.10, 0.35)
                else:
                    rec_frac = rng.uniform(0.20, 0.50)

                recovery = gross_amount * rec_frac
                net_loss = gross_amount - recovery

                if first_overdue_date is not None:
                    days_from_first_overdue = (pd.Timestamp(row["snapshot_date"]) - pd.Timestamp(first_overdue_date)).days
                else:
                    days_from_first_overdue = 0

                default_rows.append({
                    "default_event_key": default_key,
                    "customer_key": cust_key,
                    "default_date": pd.Timestamp(row["snapshot_date"]).normalize(),
                    "default_amount": round(float(gross_amount), 2),
                    "recovery_amount": round(float(recovery), 2),
                    "net_loss_amount": round(float(net_loss), 2),
                    "default_reason": reason,
                    "claim_status": rng.choice(["Open", "Closed"], p=[0.35, 0.65]),
                    "days_from_first_overdue": int(days_from_first_overdue),
                })

                defaulted_customers.add(cust_key)
                default_key += 1
                break

    return pd.DataFrame(default_rows)


def apply_default_targets(customer_month_panel, fact_default_event):
    panel = customer_month_panel.copy()
    panel["default_in_next_90d"] = 0
    panel["is_defaulted"] = 0

    default_map = fact_default_event.set_index("customer_key")["default_date"].to_dict()

    for idx, row in panel.iterrows():
        cust_key = row["customer_key"]
        snap = pd.Timestamp(row["snapshot_date"])

        if cust_key in default_map:
            dd = pd.Timestamp(default_map[cust_key])
            if snap < dd <= snap + pd.Timedelta(days=90):
                panel.at[idx, "default_in_next_90d"] = 1
            if snap >= dd:
                panel.at[idx, "is_defaulted"] = 1

    return panel