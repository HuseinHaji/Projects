from __future__ import annotations

import pandas as pd


def to_date_key(series: pd.Series) -> pd.Series:
    dt = pd.to_datetime(series)
    return dt.dt.strftime("%Y%m%d").astype(int)


def build_dim_date(
    dim_customer: pd.DataFrame,
    customer_month_panel: pd.DataFrame,
    fact_invoice: pd.DataFrame,
    fact_payment: pd.DataFrame,
    fact_default_event: pd.DataFrame,
    min_buffer_date: str = "2018-01-01",
    max_buffer_date: str = "2026-12-31",
) -> pd.DataFrame:
    """
    Build a calendar dimension covering all dates required by the warehouse.

    Parameters
    ----------
    dim_customer : pd.DataFrame
        Phase 1 customer dimension; must contain onboarding_date.
    customer_month_panel : pd.DataFrame
        Phase 1 monthly panel; must contain snapshot_date.
    fact_invoice : pd.DataFrame
        Phase 1 invoice fact; must contain invoice_date, due_date.
    fact_payment : pd.DataFrame
        Phase 1 payment fact; must contain payment_date.
    fact_default_event : pd.DataFrame
        Phase 1 default event fact; must contain default_date.
    min_buffer_date : str
        Optional lower bound safety buffer.
    max_buffer_date : str
        Optional upper bound safety buffer.

    Returns
    -------
    pd.DataFrame
        dim_date table.
    """
    candidate_dates = []

    if "onboarding_date" in dim_customer.columns:
        candidate_dates.append(pd.to_datetime(dim_customer["onboarding_date"]))

    if "snapshot_date" in customer_month_panel.columns:
        candidate_dates.append(pd.to_datetime(customer_month_panel["snapshot_date"]))

    if "invoice_date" in fact_invoice.columns:
        candidate_dates.append(pd.to_datetime(fact_invoice["invoice_date"]))

    if "due_date" in fact_invoice.columns:
        candidate_dates.append(pd.to_datetime(fact_invoice["due_date"]))

    if not fact_payment.empty and "payment_date" in fact_payment.columns:
        candidate_dates.append(pd.to_datetime(fact_payment["payment_date"]))

    if not fact_default_event.empty and "default_date" in fact_default_event.columns:
        candidate_dates.append(pd.to_datetime(fact_default_event["default_date"]))

    if not candidate_dates:
        raise ValueError("No date columns found to build dim_date.")

    min_date = min(s.min() for s in candidate_dates if len(s) > 0)
    max_date = max(s.max() for s in candidate_dates if len(s) > 0)

    min_date = min(pd.Timestamp(min_buffer_date), pd.Timestamp(min_date))
    max_date = max(pd.Timestamp(max_buffer_date), pd.Timestamp(max_date))

    date_range = pd.date_range(start=min_date, end=max_date, freq="D")
    dim_date = pd.DataFrame({"full_date": date_range})

    iso = dim_date["full_date"].dt.isocalendar()

    dim_date["date_key"] = to_date_key(dim_date["full_date"])
    dim_date["year_num"] = dim_date["full_date"].dt.year
    dim_date["quarter_num"] = dim_date["full_date"].dt.quarter
    dim_date["month_num"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["full_date"].dt.month_name()
    dim_date["year_month"] = dim_date["full_date"].dt.strftime("%Y-%m")
    dim_date["week_of_year"] = iso.week.astype(int)
    dim_date["day_of_month"] = dim_date["full_date"].dt.day
    dim_date["day_name"] = dim_date["full_date"].dt.day_name()
    dim_date["is_month_start"] = dim_date["full_date"].dt.is_month_start.astype(int)
    dim_date["is_month_end"] = dim_date["full_date"].dt.is_month_end.astype(int)
    dim_date["is_quarter_end"] = dim_date["full_date"].dt.is_quarter_end.astype(int)
    dim_date["is_year_end"] = dim_date["full_date"].dt.is_year_end.astype(int)

    cols = [
        "date_key",
        "full_date",
        "year_num",
        "quarter_num",
        "month_num",
        "month_name",
        "year_month",
        "week_of_year",
        "day_of_month",
        "day_name",
        "is_month_start",
        "is_month_end",
        "is_quarter_end",
        "is_year_end",
    ]
    dim_date = dim_date[cols].sort_values("full_date").reset_index(drop=True)
    return dim_date