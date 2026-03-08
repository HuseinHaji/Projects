from __future__ import annotations

import pandas as pd

from b2b_credit_risk_analysis.warehouse.build_dim_date import to_date_key


COUNTRY_META = {
    "Germany": {
        "country_code": "DE",
        "region_name": "DACH",
        "risk_region": "Low",
        "eur_currency_flag": 1,
    },
    "Netherlands": {
        "country_code": "NL",
        "region_name": "Western Europe",
        "risk_region": "Low",
        "eur_currency_flag": 1,
    },
    "France": {
        "country_code": "FR",
        "region_name": "Western Europe",
        "risk_region": "Medium",
        "eur_currency_flag": 1,
    },
    "Poland": {
        "country_code": "PL",
        "region_name": "CEE",
        "risk_region": "Medium",
        "eur_currency_flag": 1,
    },
    "Italy": {
        "country_code": "IT",
        "region_name": "Southern Europe",
        "risk_region": "High",
        "eur_currency_flag": 1,
    },
    "Spain": {
        "country_code": "ES",
        "region_name": "Southern Europe",
        "risk_region": "Medium",
        "eur_currency_flag": 1,
    },
    "Belgium": {
        "country_code": "BE",
        "region_name": "Western Europe",
        "risk_region": "Low",
        "eur_currency_flag": 1,
    },
    "Austria": {
        "country_code": "AT",
        "region_name": "DACH",
        "risk_region": "Low",
        "eur_currency_flag": 1,
    },
}

INDUSTRY_META = {
    "Manufacturing": {
        "industry_code": "MFG",
        "industry_risk_level": "Medium",
        "cyclical_flag": 1,
    },
    "Wholesale": {
        "industry_code": "WHL",
        "industry_risk_level": "Medium",
        "cyclical_flag": 1,
    },
    "Retail": {
        "industry_code": "RTL",
        "industry_risk_level": "Medium",
        "cyclical_flag": 1,
    },
    "Construction": {
        "industry_code": "CON",
        "industry_risk_level": "High",
        "cyclical_flag": 1,
    },
    "Logistics": {
        "industry_code": "LOG",
        "industry_risk_level": "High",
        "cyclical_flag": 1,
    },
    "Pharma": {
        "industry_code": "PHA",
        "industry_risk_level": "Low",
        "cyclical_flag": 0,
    },
    "Food & Beverage": {
        "industry_code": "FNB",
        "industry_risk_level": "Medium",
        "cyclical_flag": 0,
    },
    "Electronics": {
        "industry_code": "ELC",
        "industry_risk_level": "Medium",
        "cyclical_flag": 1,
    },
}


def build_dim_country(dim_customer_phase1: pd.DataFrame) -> pd.DataFrame:
    countries = sorted(dim_customer_phase1["country"].dropna().unique().tolist())
    rows = []

    for i, country in enumerate(countries, start=1):
        if country not in COUNTRY_META:
            raise KeyError(f"Missing COUNTRY_META mapping for '{country}'")

        meta = COUNTRY_META[country]
        rows.append(
            {
                "country_key": i,
                "country_name": country,
                "country_code": meta["country_code"],
                "region_name": meta["region_name"],
                "risk_region": meta["risk_region"],
                "eur_currency_flag": meta["eur_currency_flag"],
            }
        )

    return pd.DataFrame(rows)


def build_dim_industry(dim_customer_phase1: pd.DataFrame) -> pd.DataFrame:
    industries = sorted(dim_customer_phase1["industry"].dropna().unique().tolist())
    rows = []

    for i, industry in enumerate(industries, start=1):
        if industry not in INDUSTRY_META:
            raise KeyError(f"Missing INDUSTRY_META mapping for '{industry}'")

        meta = INDUSTRY_META[industry]
        rows.append(
            {
                "industry_key": i,
                "industry_name": industry,
                "industry_code": meta["industry_code"],
                "industry_risk_level": meta["industry_risk_level"],
                "cyclical_flag": meta["cyclical_flag"],
            }
        )

    return pd.DataFrame(rows)


def build_dim_risk_rating() -> pd.DataFrame:
    rating_rows = [
        (1, "AAA", 1, "Low", 0.0001, 0.0020),
        (2, "AA", 2, "Low", 0.0020, 0.0050),
        (3, "A", 3, "Low", 0.0050, 0.0150),
        (4, "BBB", 4, "Medium", 0.0150, 0.0350),
        (5, "BB", 5, "Medium", 0.0350, 0.0800),
        (6, "B", 6, "High", 0.0800, 0.1800),
        (7, "CCC", 7, "High", 0.1800, 0.5000),
    ]
    return pd.DataFrame(
        rating_rows,
        columns=[
            "rating_key",
            "rating_code",
            "rating_score",
            "rating_bucket",
            "pd_band_low",
            "pd_band_high",
        ],
    )


def build_dim_customer(
    dim_customer_phase1: pd.DataFrame,
    dim_country: pd.DataFrame,
    dim_industry: pd.DataFrame,
    dim_date: pd.DataFrame,
) -> pd.DataFrame:
    dim_customer = dim_customer_phase1.copy()

    dim_customer["onboarding_date"] = pd.to_datetime(dim_customer["onboarding_date"])
    dim_customer["onboarding_date_key"] = to_date_key(dim_customer["onboarding_date"])

    valid_date_keys = set(dim_date["date_key"].tolist())
    missing_date_keys = set(dim_customer["onboarding_date_key"].unique()) - valid_date_keys
    if missing_date_keys:
        raise ValueError(
            f"Found onboarding_date_key values not present in dim_date: "
            f"{sorted(list(missing_date_keys))[:10]}"
        )

    dim_customer = dim_customer.merge(
        dim_country[["country_key", "country_name"]],
        left_on="country",
        right_on="country_name",
        how="left",
        validate="many_to_one",
    )

    dim_customer = dim_customer.merge(
        dim_industry[["industry_key", "industry_name"]],
        left_on="industry",
        right_on="industry_name",
        how="left",
        validate="many_to_one",
    )

    if dim_customer["country_key"].isna().any():
        missing = dim_customer.loc[dim_customer["country_key"].isna(), "country"].unique()
        raise ValueError(f"Missing country_key mapping for: {missing.tolist()}")

    if dim_customer["industry_key"].isna().any():
        missing = dim_customer.loc[dim_customer["industry_key"].isna(), "industry"].unique()
        raise ValueError(f"Missing industry_key mapping for: {missing.tolist()}")

    final = dim_customer[
        [
            "customer_key",
            "customer_id",
            "customer_name",
            "country_key",
            "industry_key",
            "company_size",
            "years_in_business",
            "annual_revenue_eur",
            "employee_count",
            "onboarding_date_key",
            "legal_form",
            "parent_group_flag",
            "base_risk_score",
            "base_insured_limit",
            "active_flag",
        ]
    ].copy()

    final["country_key"] = final["country_key"].astype(int)
    final["industry_key"] = final["industry_key"].astype(int)
    final["onboarding_date_key"] = final["onboarding_date_key"].astype(int)

    final = final.sort_values("customer_key").reset_index(drop=True)
    return final