import numpy as np
import pandas as pd

from b2b_credit_risk_analysis.config import COUNTRY_WEIGHTS, INDUSTRY_WEIGHTS, SIZE_WEIGHTS

def sample_weighted(mapping, n, rng):
    keys = list(mapping.keys())
    probs = list(mapping.values())
    return rng.choice(keys, size=n, p=probs)

def generate_customer_dimension(n_customers=10000, seed=42):
    rng = np.random.default_rng(seed)

    countries = sample_weighted(COUNTRY_WEIGHTS, n_customers, rng)
    industries = sample_weighted(INDUSTRY_WEIGHTS, n_customers, rng)
    sizes = sample_weighted(SIZE_WEIGHTS, n_customers, rng)

    years_in_business = np.clip(rng.gamma(shape=3.8, scale=4.2, size=n_customers).astype(int) + 1, 1, 60)

    onboarding_dates = pd.to_datetime(
        rng.choice(pd.date_range("2018-01-01", "2025-06-30", freq="D"), size=n_customers)
    )

    parent_group_flag = rng.binomial(1, 0.28, size=n_customers)

    revenue_ranges = {
        "Small": (5e5, 8e6),
        "Medium": (5e6, 4e7),
        "Large": (3e7, 2.5e8),
        "Enterprise": (2e8, 2e9),
    }

    legal_forms = {
        "Germany": ["GmbH", "AG"],
        "Netherlands": ["BV", "NV"],
        "France": ["SARL", "SAS"],
        "Poland": ["Sp. z o.o.", "S.A."],
        "Italy": ["SRL", "SpA"],
        "Spain": ["SL", "SA"],
        "Belgium": ["BV", "NV"],
        "Austria": ["GmbH", "AG"],
    }

    industry_adj = {
        "Manufacturing": 0.00,
        "Wholesale": 0.05,
        "Retail": 0.15,
        "Construction": 0.35,
        "Logistics": 0.20,
        "Pharma": -0.20,
        "Food & Beverage": 0.05,
        "Electronics": 0.08,
    }

    country_adj = {
        "Germany": -0.10,
        "Netherlands": -0.08,
        "France": 0.00,
        "Poland": 0.12,
        "Italy": 0.20,
        "Spain": 0.10,
        "Belgium": -0.03,
        "Austria": -0.05,
    }

    size_adj = {
        "Small": 0.22,
        "Medium": 0.08,
        "Large": -0.08,
        "Enterprise": -0.18,
    }

    annual_revenue = []
    employee_count = []
    legal_form_list = []
    base_risk_score = []
    base_insured_limit = []
    customer_name = []

    for i in range(n_customers):
        size = sizes[i]
        country = countries[i]
        industry = industries[i]
        yib = years_in_business[i]

        lo, hi = revenue_ranges[size]
        rev = np.exp(rng.normal(np.log(np.sqrt(lo * hi)), 0.7))
        rev = float(np.clip(rev, lo, hi))
        annual_revenue.append(rev)

        emp = int(np.clip(rev / rng.uniform(120000, 220000), 3, 25000))
        employee_count.append(emp)

        lf = rng.choice(legal_forms[country])
        legal_form_list.append(lf)

        score = (
            industry_adj[industry]
            + country_adj[country]
            + size_adj[size]
            - 0.04 * np.log1p(yib)
            + rng.normal(0, 0.35)
        )
        base_risk_score.append(score)

        limit_pct = rng.uniform(0.02, 0.12)
        if size in ["Large", "Enterprise"]:
            limit_pct *= 1.15
        if industry == "Construction":
            limit_pct *= 0.90
        limit = rev * limit_pct
        base_insured_limit.append(limit)

        customer_name.append(f"{country[:3].upper()}_{industry[:4].upper()}_{i+1:05d}")

    dim_customer = pd.DataFrame({
        "customer_key": np.arange(1, n_customers + 1),
        "customer_id": [f"CUST_{i:05d}" for i in range(1, n_customers + 1)],
        "customer_name": customer_name,
        "country": countries,
        "industry": industries,
        "company_size": sizes,
        "years_in_business": years_in_business,
        "annual_revenue_eur": annual_revenue,
        "employee_count": employee_count,
        "onboarding_date": onboarding_dates,
        "legal_form": legal_form_list,
        "parent_group_flag": parent_group_flag,
        "base_risk_score": base_risk_score,
        "base_insured_limit": base_insured_limit,
        "active_flag": 1,
    })

    return dim_customer

def map_rating(latent_score: float):
    if latent_score <= -0.9:
        return "AAA", 1
    elif latent_score <= -0.5:
        return "AA", 2
    elif latent_score <= -0.1:
        return "A", 3
    elif latent_score <= 0.35:
        return "BBB", 4
    elif latent_score <= 0.8:
        return "BB", 5
    elif latent_score <= 1.3:
        return "B", 6
    else:
        return "CCC", 7