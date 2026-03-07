from b2b_credit_risk_analysis.data_generation.customers import generate_customer_dimension
from b2b_credit_risk_analysis.data_generation.customer_month import generate_customer_month_panel
from b2b_credit_risk_analysis.data_generation.invoices import generate_invoices, attach_due_month_context
from b2b_credit_risk_analysis.data_generation.payments import generate_payments
from b2b_credit_risk_analysis.data_generation.defaults import generate_default_events, apply_default_targets
from b2b_credit_risk_analysis.data_generation.finalize import finalize_invoice_status


def run_phase1_generation():
    dim_customer = generate_customer_dimension(n_customers=10_000, seed=42)

    customer_month_panel = generate_customer_month_panel(
        dim_customer=dim_customer,
        start="2022-01-31",
        end="2025-12-31",
        seed=42,
    )

    fact_invoice = generate_invoices(customer_month_panel, seed=42)
    invoices_with_context = attach_due_month_context(fact_invoice, customer_month_panel)
    fact_payment = generate_payments(invoices_with_context, seed=42)

    fact_default_event = generate_default_events(customer_month_panel, seed=42)
    customer_month_panel = apply_default_targets(customer_month_panel, fact_default_event)

    fact_invoice = finalize_invoice_status(fact_invoice, fact_payment, fact_default_event)

    return {
        "dim_customer": dim_customer,
        "customer_month_panel": customer_month_panel,
        "fact_invoice": fact_invoice,
        "fact_payment": fact_payment,
        "fact_default_event": fact_default_event,
    }


if __name__ == "__main__":
    outputs = run_phase1_generation()
    for name, df in outputs.items():
        print(f"{name}: {df.shape}")