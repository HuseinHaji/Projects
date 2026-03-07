import numpy as np
import pandas as pd

from b2b_credit_risk_analysis.data_generation.customers import map_rating


def generate_customer_month_panel(dim_customer, start="2022-01-31", end="2025-12-31", seed=42):
    rng = np.random.default_rng(seed)
    month_ends = pd.date_range(start, end, freq="M")

    seasonality = {
        1: 0.92, 2: 0.95, 3: 1.00, 4: 1.02, 5: 1.03, 6: 1.05,
        7: 0.98, 8: 0.94, 9: 1.01, 10: 1.06, 11: 1.08, 12: 0.96,
    }

    rows = []

    for row in dim_customer.itertuples(index=False):
        latent_prev = row.base_risk_score + rng.normal(0, 0.15)
        dpd_prev = max(0, rng.normal(8 + 7 * max(row.base_risk_score, 0), 4))
        util_prev = np.clip(rng.normal(0.45 + 0.08 * row.base_risk_score, 0.10), 0.05, 1.10)
        prev_rating_score = None
        defaulted = 0

        annual_rev = row.annual_revenue_eur
        monthly_base_sales = annual_rev / 12

        for dt in month_ends:
            if dt < pd.Timestamp(row.onboarding_date).replace(day=1) + pd.offsets.MonthEnd(0):
                continue

            macro_shock = rng.normal(0, 0.08)
            idio_shock = rng.normal(0, 0.16)
            stress_flag = int(rng.random() < (0.04 + 0.04 * max(row.base_risk_score, 0)))

            stress_carry = 0.35 if stress_flag else 0.0

            latent_state = (
                0.72 * latent_prev
                + 0.28 * row.base_risk_score
                + macro_shock
                + idio_shock
                + stress_carry
            )

            if defaulted == 1:
                latent_state += 0.8

            seasonal_mult = seasonality[dt.month]
            sales_noise = rng.normal(1.0, 0.10)

            sales_penalty = 1.0
            if latent_state > 1.0:
                sales_penalty -= min(0.22, 0.06 * (latent_state - 1.0))

            monthly_sales = max(0, monthly_base_sales * seasonal_mult * sales_noise * sales_penalty)

            size_invoice_lambda = {
                "Small": 4,
                "Medium": 10,
                "Large": 26,
                "Enterprise": 65,
            }[row.company_size]

            invoice_count = max(1, rng.poisson(size_invoice_lambda * seasonal_mult * sales_penalty))

            insured_limit = row.base_insured_limit * np.clip(rng.normal(1.0, 0.04), 0.85, 1.15)

            util = np.clip(
                0.58 * util_prev
                + 0.20 * np.clip(monthly_sales / max(insured_limit, 1), 0, 2.5)
                + 0.14 * max(latent_state, -0.5)
                + rng.normal(0, 0.06),
                0.03, 1.25
            )

            current_exposure = max(0, insured_limit * util * rng.uniform(0.90, 1.12))

            avg_dpd = max(
                0,
                0.52 * dpd_prev
                + 10
                + 10 * max(latent_state, 0)
                + 8 * stress_flag
                + rng.normal(0, 4)
            )

            max_dpd = int(max(avg_dpd, avg_dpd + abs(rng.normal(8, 10))))

            overdue_ratio = np.clip(
                0.02
                + 0.06 * max(latent_state, 0)
                + 0.004 * avg_dpd
                + 0.08 * max(util - 0.85, 0)
                + rng.normal(0, 0.03),
                0.0, 1.0
            )

            overdue_exposure = min(current_exposure, current_exposure * overdue_ratio)
            open_invoice_count = int(max(1, invoice_count * rng.uniform(0.6, 1.4)))

            rating_code, rating_score = map_rating(latent_state)
            notch_change = 0 if prev_rating_score is None else rating_score - prev_rating_score
            downgrade_flag = int(notch_change > 0)

            warning_flag = int(
                (avg_dpd >= 25)
                or (util >= 0.90)
                or (overdue_ratio >= 0.25)
                or (downgrade_flag == 1)
            )

            rows.append({
                "customer_key": row.customer_key,
                "snapshot_date": dt.normalize(),
                "year_month": dt.strftime("%Y-%m"),
                "monthly_sales_estimate": round(monthly_sales, 2),
                "invoice_count_month": int(invoice_count),
                "current_exposure": round(current_exposure, 2),
                "overdue_exposure": round(overdue_exposure, 2),
                "overdue_ratio": round(overdue_ratio, 4),
                "insured_limit": round(insured_limit, 2),
                "utilization_ratio": round(util, 4),
                "avg_days_past_due": round(avg_dpd, 2),
                "max_days_past_due": int(max_dpd),
                "open_invoice_count": int(open_invoice_count),
                "rating_code": rating_code,
                "rating_score": int(rating_score),
                "notch_change": int(notch_change),
                "downgrade_flag": int(downgrade_flag),
                "stress_flag": int(stress_flag),
                "warning_flag": int(warning_flag),
                "default_in_next_90d": 0,
                "is_defaulted": int(defaulted),
                "latent_state": round(latent_state, 4),
            })

            latent_prev = latent_state
            dpd_prev = avg_dpd
            util_prev = util
            prev_rating_score = rating_score

    panel = pd.DataFrame(rows)
    return panel


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