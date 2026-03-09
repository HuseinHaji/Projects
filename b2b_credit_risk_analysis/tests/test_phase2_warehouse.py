import pandas as pd

from b2b_credit_risk_analysis.warehouse.run_phase2 import build_phase2_tables


def test_phase2_build_smoke():
    dim_customer_phase1 = pd.DataFrame(
        {
            "customer_key": [1],
            "customer_id": ["CUST_00001"],
            "customer_name": ["TEST_CO"],
            "country": ["Germany"],
            "industry": ["Manufacturing"],
            "company_size": ["Medium"],
            "years_in_business": [10],
            "annual_revenue_eur": [10000000.0],
            "employee_count": [50],
            "onboarding_date": ["2022-01-01"],
            "legal_form": ["GmbH"],
            "parent_group_flag": [0],
            "base_risk_score": [0.1],
            "base_insured_limit": [500000.0],
            "active_flag": [1],
        }
    )

    customer_month_panel_phase1 = pd.DataFrame(
        {
            "customer_key": [1],
            "snapshot_date": ["2022-01-31"],
            "year_month": ["2022-01"],
            "monthly_sales_estimate": [100000.0],
            "invoice_count_month": [5],
            "current_exposure": [200000.0],
            "overdue_exposure": [10000.0],
            "overdue_ratio": [0.05],
            "insured_limit": [500000.0],
            "utilization_ratio": [0.4],
            "avg_days_past_due": [8.0],
            "max_days_past_due": [15],
            "open_invoice_count": [4],
            "rating_code": ["BBB"],
            "rating_score": [4],
            "notch_change": [0],
            "downgrade_flag": [0],
            "stress_flag": [0],
            "warning_flag": [0],
            "default_in_next_90d": [0],
            "is_defaulted": [0],
        }
    )

    fact_invoice_phase1 = pd.DataFrame(
        {
            "invoice_key": [1],
            "invoice_id": ["INV_000000001"],
            "customer_key": [1],
            "invoice_date": ["2022-01-15"],
            "due_date": ["2022-02-14"],
            "invoice_amount": [25000.0],
            "currency_code": ["EUR"],
            "payment_terms_days": [30],
            "product_category": ["B2B Goods/Services"],
            "insured_flag": [1],
            "invoice_status": ["Paid"],
        }
    )

    fact_payment_phase1 = pd.DataFrame(
        {
            "payment_key": [1],
            "invoice_key": [1],
            "payment_date": ["2022-02-16"],
            "payment_amount": [25000.0],
            "days_late": [2],
            "partial_payment_flag": [0],
            "payment_status": ["Paid"],
            "recovered_after_default_flag": [0],
        }
    )

    fact_default_event_phase1 = pd.DataFrame(
        columns=[
            "default_event_key",
            "customer_key",
            "default_date",
            "default_amount",
            "recovery_amount",
            "net_loss_amount",
            "default_reason",
            "claim_status",
            "days_from_first_overdue",
        ]
    )

    tables = build_phase2_tables(
        dim_customer_phase1=dim_customer_phase1,
        customer_month_panel_phase1=customer_month_panel_phase1,
        fact_invoice_phase1=fact_invoice_phase1,
        fact_payment_phase1=fact_payment_phase1,
        fact_default_event_phase1=fact_default_event_phase1,
    )

    assert "dim_date" in tables
    assert "dim_customer" in tables
    assert "fact_exposure_snapshot" in tables
    assert tables["dim_customer"].shape[0] == 1
    assert tables["fact_exposure_snapshot"].shape[0] == 1
    assert tables["fact_invoice"].shape[0] == 1
    assert tables["fact_payment"].shape[0] == 1