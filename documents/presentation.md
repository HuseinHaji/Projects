---
theme: default
title: Market Stress Early-Warning System
info: Monitoring High-Volatility Regimes in Equity Markets
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
---

# Market Stress Early-Warning System
### Monitoring High-Volatility Regimes in Equity Markets

Huseyn Hajiyev
EPP Project

---

# Motivation

Financial markets periodically experience **high-volatility regimes**.

These periods are associated with:

- large price movements
- higher uncertainty
- increased systemic risk

### Research Question

Can **volatility-based indicators** help predict stress regimes in the S&P 500?

---

# Project Goal

Build a **reproducible pipeline** that:

- downloads and cleans S&P 500 data
- constructs volatility-based predictors
- estimates a logistic regression model
- evaluates predictions using an expanding-window backtest
- automatically exports figures and tables to the paper

---

# Data

**Source**

Daily S&P 500 data from **Stooq**

**Constructed variables**

- returns
- rolling volatility
- lagged predictors
- stress regime indicator

The full workflow is automated using **pytask**.

---

# Methodology

**Model**

Logistic Regression

**Evaluation Design**

- expanding-window backtest
- model refitting through time
- out-of-sample probability predictions

**Metrics**

- AUC
- Average Precision
- Brier Score

---

# Why Expanding Window?

This setup ensures realistic evaluation:

- only past information is used
- mimics real-time forecasting
- avoids look-ahead bias
- produces credible out-of-sample results

---

# ROC Curve

<div class="grid grid-cols-2 gap-6">

<div>

The ROC curve summarizes classification performance across thresholds.

Higher AUC indicates stronger ability to distinguish stress vs calm regimes.

</div>

<div>

![](./public/roc_curve.png)

</div>

</div>

---

# Predicted Stress Probability

<div class="grid grid-cols-2 gap-6">

<div>

The model assigns **higher stress probabilities during turbulent periods**.

These spikes correspond to episodes of elevated volatility.

</div>

<div>

![](./public/predicted_probability.png)

</div>

</div>

---

# Baseline Comparison

<div class="grid grid-cols-2 gap-6">

<div>

Models compared:

- volatility-state logistic regression
- returns-only logistic regression
- naive volatility percentile rule

</div>

<div>

![](./public/model_comparison_auc.png)

</div>

</div>

---

# Stress Regimes in the Data

<div class="grid grid-cols-2 gap-6">

<div>

The stress indicator is derived from **rolling volatility dynamics**.

Periods where volatility exceeds a threshold are classified as stress regimes.

</div>

<div>

![](./public/volatility_stress.png)

</div>

</div>

---

# Key Takeaways

- Volatility indicators contain **predictive information about stress regimes**
- A simple logistic regression provides **interpretable probability forecasts**
- Expanding-window evaluation provides **realistic model assessment**
- Reproducible pipelines improve **research transparency**

---

# Limitations & Extensions

**Current scope**

- single market (S&P 500)
- simple model specification
- limited feature set

**Possible extensions**

- macro-financial predictors
- alternative stress definitions
- nonlinear ML models
- multi-asset analysis

---

# Thank You
