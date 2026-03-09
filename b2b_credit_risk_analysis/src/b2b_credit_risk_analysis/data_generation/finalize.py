import numpy as np
import pandas as pd

def finalize_invoice_status(fact_invoice, fact_payment, fact_default_event):
    invoices = fact_invoice.copy()

    paid_amount = fact_payment.groupby("invoice_key", as_index=False)["payment_amount"].sum()
    paid_amount = paid_amount.rename(columns={"payment_amount": "total_paid_amount"})

    invoices = invoices.merge(paid_amount, on="invoice_key", how="left")
    invoices["total_paid_amount"] = invoices["total_paid_amount"].fillna(0)

    defaulted_customers = set(fact_default_event["customer_key"].unique())
    default_dates = fact_default_event.set_index("customer_key")["default_date"].to_dict()

    statuses = []
    for row in invoices.itertuples(index=False):
        if row.total_paid_amount >= row.invoice_amount:
            statuses.append("Paid")
        elif row.total_paid_amount > 0:
            statuses.append("Overdue")
        else:
            if row.customer_key in defaulted_customers:
                if pd.Timestamp(row.due_date) <= pd.Timestamp(default_dates[row.customer_key]):
                    statuses.append("Defaulted")
                else:
                    statuses.append("Open")
            else:
                statuses.append("Open")

    invoices["invoice_status"] = statuses
    return invoices