from __future__ import annotations

import pandas as pd

from b2b_credit_risk_analysis.warehouse.build_dim_date import to_date_key


def build_fact_exposure_snapshot(
    customer_month_panel_phase1: pd.DataFrame,
    dim_risk_rating: pd.DataFrame,
) -> pd.DataFrame:
    fact = customer_month_panel_phase1.copy()

    fact["snapshot_date"] = pd.to_datetime(fact["snapshot_date"])
    fact["snapshot_date_key"] = to_date_key(fact["snapshot_date"])

    fact = fact.merge(
        dim_risk_rating[["rating_key", "rating_code"]],
        on="rating_code",
        how="left",
        validate="many_to_one",
    )

    if fact["rating_key"].isna().any():
        missing = fact.loc[fact["rating_key"].isna(), "rating_code"].unique()
        raise ValueError(f"Missing rating_key mapping for rating_code values: {missing.tolist()}")

    fact.insert(0, "exposure_snapshot_key", range(1, len(fact) + 1))
    fact["rating_key"] = fact["rating_key"].astype(int)
    fact["snapshot_date_key"] = fact["snapshot_date_key"].astype(int)

    final = fact[
        [
            "exposure_snapshot_key",
            "customer_key",
            "snapshot_date_key",
            "rating_key",
            "monthly_sales_estimate",
            "invoice_count_month",
            "current_exposure",
            "overdue_exposure",
            "overdue_ratio",
            "insured_limit",
            "utilization_ratio",
            "avg_days_past_due",
            "max_days_past_due",
            "open_invoice_count",
            "notch_change",
            "downgrade_flag",
            "stress_flag",
            "warning_flag",
            "default_in_next_90d",
            "is_defaulted",
        ]
    ].copy()

    return final


def build_fact_invoice(fact_invoice_phase1: pd.DataFrame) -> pd.DataFrame:
    fact = fact_invoice_phase1.copy()

    fact["invoice_date"] = pd.to_datetime(fact["invoice_date"])
    fact["due_date"] = pd.to_datetime(fact["due_date"])
    fact["invoice_date_key"] = to_date_key(fact["invoice_date"])
    fact["due_date_key"] = to_date_key(fact["due_date"])

    final = fact[
        [
            "invoice_key",
            "invoice_id",
            "customer_key",
            "invoice_date_key",
            "due_date_key",
            "invoice_amount",
            "currency_code",
            "payment_terms_days",
            "product_category",
            "insured_flag",
            "invoice_status",
        ]
    ].copy()

    final["invoice_date_key"] = final["invoice_date_key"].astype(int)
    final["due_date_key"] = final["due_date_key"].astype(int)

    return final


def build_fact_payment(fact_payment_phase1: pd.DataFrame) -> pd.DataFrame:
    fact = fact_payment_phase1.copy()

    if fact.empty:
        return pd.DataFrame(
            columns=[
                "payment_key",
                "invoice_key",
                "payment_date_key",
                "payment_amount",
                "days_late",
                "partial_payment_flag",
                "payment_status",
                "recovered_after_default_flag",
            ]
        )

    fact["payment_date"] = pd.to_datetime(fact["payment_date"])
    fact["payment_date_key"] = to_date_key(fact["payment_date"])

    final = fact[
        [
            "payment_key",
            "invoice_key",
            "payment_date_key",
            "payment_amount",
            "days_late",
            "partial_payment_flag",
            "payment_status",
            "recovered_after_default_flag",
        ]
    ].copy()

    final["payment_date_key"] = final["payment_date_key"].astype(int)
    return final


def build_fact_default_event(fact_default_event_phase1: pd.DataFrame) -> pd.DataFrame:
    fact = fact_default_event_phase1.copy()

    if fact.empty:
        return pd.DataFrame(
            columns=[
                "default_event_key",
                "customer_key",
                "default_date_key",
                "default_amount",
                "recovery_amount",
                "net_loss_amount",
                "default_reason",
                "claim_status",
                "days_from_first_overdue",
            ]
        )

    fact["default_date"] = pd.to_datetime(fact["default_date"])
    fact["default_date_key"] = to_date_key(fact["default_date"])

    final = fact[
        [
            "default_event_key",
            "customer_key",
            "default_date_key",
            "default_amount",
            "recovery_amount",
            "net_loss_amount",
            "default_reason",
            "claim_status",
            "days_from_first_overdue",
        ]
    ].copy()

    final["default_date_key"] = final["default_date_key"].astype(int)
    return final


def build_fact_rating_history(
    customer_month_panel_phase1: pd.DataFrame,
    dim_risk_rating: pd.DataFrame,
) -> pd.DataFrame:
    fact = customer_month_panel_phase1.copy()

    fact["snapshot_date"] = pd.to_datetime(fact["snapshot_date"])
    fact["snapshot_date_key"] = to_date_key(fact["snapshot_date"])

    fact = fact.merge(
        dim_risk_rating[["rating_key", "rating_code"]],
        on="rating_code",
        how="left",
        validate="many_to_one",
    )

    if fact["rating_key"].isna().any():
        missing = fact.loc[fact["rating_key"].isna(), "rating_code"].unique()
        raise ValueError(f"Missing rating_key mapping for rating_code values: {missing.tolist()}")

    fact.insert(0, "rating_history_key", range(1, len(fact) + 1))
    fact["rating_key"] = fact["rating_key"].astype(int)
    fact["snapshot_date_key"] = fact["snapshot_date_key"].astype(int)

    final = fact[
        [
            "rating_history_key",
            "customer_key",
            "snapshot_date_key",
            "rating_key",
            "rating_score",
            "notch_change",
            "downgrade_flag",
        ]
    ].copy()

    return final