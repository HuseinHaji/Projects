from pathlib import Path

from b2b_credit_risk_analysis.data_generation.customers import generate_customer_dimension
from b2b_credit_risk_analysis.data_generation.customer_month import generate_customer_month_panel
from b2b_credit_risk_analysis.data_generation.invoices import generate_invoices, attach_due_month_context
from b2b_credit_risk_analysis.data_generation.payments import generate_payments
from b2b_credit_risk_analysis.data_generation.defaults import generate_default_events, apply_default_targets
from b2b_credit_risk_analysis.data_generation.finalize import finalize_invoice_status


def prepare_public_exports(
    dim_customer,
    customer_month_panel,
    fact_invoice,
    fact_payment,  
    fact_default_event,
):
    # 1) dim_customer.csv
    dim_customer_export = dim_customer.copy()

    # 2) customer_month_panel.csv
    
    customer_month_panel_export = customer_month_panel.copy()
    if "latent_state" in customer_month_panel_export.columns:
        customer_month_panel_export = customer_month_panel_export.drop(columns=["latent_state"])

    # 3) fact_invoice.csv
    
    fact_invoice_export = fact_invoice.copy()
    if "snapshot_month" in fact_invoice_export.columns:
        fact_invoice_export = fact_invoice_export.drop(columns=["snapshot_month"])

    # 4) fact_payment.csv
    fact_payment_export = fact_payment.copy()

    # 5) fact_default_event.csv
    fact_default_event_export = fact_default_event.copy()

    return {
        "dim_customer": dim_customer_export,
        "customer_month_panel": customer_month_panel_export,
        "fact_invoice": fact_invoice_export,
        "fact_payment": fact_payment_export,
        "fact_default_event": fact_default_event_export,
    }


def save_outputs(outputs: dict, output_dir: str = "b2b_credit_risk_analysis/data/processed/phase1"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for name, df in outputs.items():
        file_path = output_path / f"{name}.csv"
        df.to_csv(file_path, index=False)
        print(f"Saved {name}: {df.shape} -> {file_path}")


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

    public_exports = prepare_public_exports(
        dim_customer=dim_customer,
        customer_month_panel=customer_month_panel,
        fact_invoice=fact_invoice,
        fact_payment=fact_payment,
        fact_default_event=fact_default_event,
    )

    return public_exports


if __name__ == "__main__":
    outputs = run_phase1_generation()
    save_outputs(outputs)