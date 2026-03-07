import numpy as np
import pandas as pd

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