# config.py
N_CUSTOMERS = 10000
START_DATE = "2022-01-01"
END_DATE = "2025-12-31"

COUNTRY_WEIGHTS = {
    "Germany": 0.38,
    "Netherlands": 0.10,
    "France": 0.12,
    "Poland": 0.12,
    "Italy": 0.10,
    "Spain": 0.08,
    "Belgium": 0.05,
    "Austria": 0.05,
}

INDUSTRY_WEIGHTS = {
    "Manufacturing": 0.22,
    "Wholesale": 0.18,
    "Retail": 0.14,
    "Construction": 0.12,
    "Logistics": 0.12,
    "Pharma": 0.08,
    "Food & Beverage": 0.08,
    "Electronics": 0.06,
}

SIZE_WEIGHTS = {
    "Small": 0.34,
    "Medium": 0.36,
    "Large": 0.20,
    "Enterprise": 0.10,
}