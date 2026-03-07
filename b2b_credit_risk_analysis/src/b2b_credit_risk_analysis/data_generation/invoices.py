import numpy as np
import pandas as pd

def generate_invoices(customer_month_panel, seed=42):
    rng = np.random.default_rng(seed)
    invoice_rows = []
    invoice_key = 1

    terms_by_size = {
        "Small": [30, 45],
        "Medium": [30, 45, 60],
        "Large": [45, 60, 90],
        "Enterprise": [60, 90],
    }

    for row in customer_month_panel.itertuples(index=False):
        ym_start = pd.Timestamp(row.snapshot_date).replace(day=1)
        ym_end = pd.Timestamp(row.snapshot_date)

        n_inv = int(row.invoice_count_month)
        total_sales = max(row.monthly_sales_estimate, 1.0)

        weights = rng.gamma(shape=2.0, scale=1.0, size=n_inv)
        weights = weights / weights.sum()

        amounts = np.maximum(100, total_sales * weights)

        for amount in amounts:
            invoice_date = ym_start + pd.Timedelta(days=int(rng.integers(0, min(ym_end.day, 28))))
            payment_terms = int(rng.choice([30, 45, 60, 90], p=[0.35, 0.30, 0.25, 0.10]))
            due_date = invoice_date + pd.Timedelta(days=payment_terms)

            insured_flag = int(rng.random() < 0.93)

            invoice_rows.append({
                "invoice_key": invoice_key,
                "invoice_id": f"INV_{invoice_key:09d}",
                "customer_key": row.customer_key,
                "invoice_date": invoice_date.normalize(),
                "due_date": due_date.normalize(),
                "invoice_amount": round(float(amount), 2),
                "currency_code": "EUR",
                "payment_terms_days": payment_terms,
                "product_category": "B2B Goods/Services",
                "insured_flag": insured_flag,
                "invoice_status": "Open",
                "snapshot_month": row.year_month,
            })
            invoice_key += 1

    return pd.DataFrame(invoice_rows)

def attach_due_month_context(invoices, customer_month_panel):
    panel = customer_month_panel.copy()
    panel["year_month"] = pd.to_datetime(panel["snapshot_date"]).dt.strftime("%Y-%m")

    invoices = invoices.copy()
    invoices["due_year_month"] = pd.to_datetime(invoices["due_date"]).dt.to_period("M").astype(str)

    ctx = panel[[
        "customer_key", "year_month", "avg_days_past_due", "overdue_ratio",
        "utilization_ratio", "rating_score", "stress_flag", "warning_flag", "latent_state"
    ]].rename(columns={"year_month": "due_year_month"})

    invoices = invoices.merge(
        ctx,
        on=["customer_key", "due_year_month"],
        how="left"
    )

    return invoices