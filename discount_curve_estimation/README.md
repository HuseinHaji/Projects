# Discount Curve Estimation from Coupon Bonds
### Monte Carlo Assessment of Smoothness-Regularized Term Structure Estimation

Implementation of a **smoothness-regularized discount curve estimator** based on the framework of **Filipović–Pelger–Ye (2022)**.  
The project evaluates the estimator using Monte Carlo simulations and compares it to the **Nelson–Siegel–Svensson (NSS)** benchmark.

The objective is to recover the **zero-coupon discount curve** from prices of coupon-bearing bonds, an inherently **ill-posed inverse problem** in financial econometrics.

---

## Authors

**Huseyn Hajiyev**  
**Berke Pehlivan**  
**Elvin Nasibov**

University of Bonn  
M.Sc. Economics — Econometrics & Statistics

Supervisors:

- Dennis Schroers  
- Egshiglen Batbayar

---

## Project Overview

In practice, the yield curve is **not directly observable** and must be inferred from a cross-section of coupon bond prices.

This introduces several challenges:

- overlapping bond cash flows  
- limited maturity coverage  
- measurement noise in prices  
- underdetermined pricing equations

To address this, the **Filipović–Pelger–Ye framework** introduces a **smoothness regularization penalty** that stabilizes the estimation problem and yields a **kernel ridge regression estimator**.

This project evaluates the **finite-sample behavior of this estimator** using controlled Monte Carlo simulations.

---

## Methodology

The estimator solves the regularized optimization problem:

\[
\min_g \sum_{i=1}^{M} \omega_i (P_i - P_i^g)^2 + \lambda \|g\|^2
\]

where

- \(P_i\) = observed bond price  
- \(P_i^g\) = model price implied by discount curve \(g\)  
- \(ω_i\) = duration-based weights  
- \(λ\) = smoothness regularization parameter  

The smoothness penalty induces a **Reproducing Kernel Hilbert Space (RKHS)** representation.

Using the **representer theorem**, the estimator can be written as:

\[
\hat g(x) = 1 + \sum_{j=1}^{N} k(x, x_j) \beta_j
\]

with coefficients

\[
\beta = C^T (C K C^T + \Lambda)^{-1}(P - C1)
\]

This reduces the infinite-dimensional estimation problem to **finite-dimensional linear algebra operations**.

---

## Simulation Design

Monte Carlo experiment:

- **Replications:** 250  
- **Maturity grid:** 0.5 – 30 years (semiannual)  
- **Bond universe**
  - maturities: 1–30 years  
  - coupon rates: 0–5%  
  - semiannual coupons  
- **Price noise:** Gaussian noise (5% of mean price)

Hyperparameters are selected using **K-fold cross-validation** minimizing pricing RMSE.

---

## Benchmark Model

The estimator is compared with the widely used **Nelson–Siegel–Svensson (NSS)** yield curve specification.

Evaluation metrics include:

- pricing RMSE
- yield RMSE (basis points)
- curve recovery diagnostics
- estimator stability

---

## Repository Structure

```
discount-curve-estimation

paper/
    discount_curve_estimation_from_coupon_bonds.pdf

code/
    monte_carlo_simulation.R
    post_processing_plots.R

results/
    figures/
    tables/

README.md
```

---

## Running the Project

### 1. Run Monte Carlo simulation

```
Rscript code/monte_carlo_simulation.R
```

Outputs will be generated in:

```
mc_out_fpy_vs_nss/
```

---

### 2. Generate figures and summary tables

```
Rscript code/post_processing_plots.R
```

This produces:

- yield curve recovery plots
- discount curve recovery
- identification maps of yield errors
- observed vs fitted bond prices
- RMSE summary tables

---

## Example Outputs

The project generates several diagnostic plots including:

- Monte Carlo yield curve recovery bands
- discount factor recovery
- identification maps by maturity
- price fit diagnostics
- RMSE performance summaries

---

## Key Findings

The smoothness-regularized estimator:

- stabilizes discount curve estimation
- improves pricing accuracy
- reduces estimator instability

Compared with the Nelson–Siegel–Svensson specification, the method demonstrates stronger robustness under noisy price observations.

---

## Technologies Used

- R
- data.table
- ggplot2
- numerical linear algebra
- Monte Carlo simulation
- kernel ridge regression

---

## Research Context

This project was developed as part of the **Research Module in Econometrics and Statistics** at the **University of Bonn**.

The analysis focuses on **cross-sectional term-structure estimation**, isolating the role of **regularization and identification** in discount curve recovery.

---

## Keywords

Financial Econometrics  
Yield Curve Estimation  
Term Structure of Interest Rates  
Kernel Ridge Regression  
Smoothness Regularization  
Monte Carlo Simulation  
Nelson–Siegel–Svensson