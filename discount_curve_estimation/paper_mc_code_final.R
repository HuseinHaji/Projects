# ============================================================
# Discount Curve Estimation from Coupon Bonds:
# A Monte Carlo Assessment of Smoothness Regularization
#
# R code to reproduce the Monte Carlo simulations and outputs
# reported in the accompanying paper (Research Module).
#
# Authors:
#   Berke Pehlivan (50266988)
#   Elvin Nasibov  (50312616)
#   Huseyn Hajiyev (50311073)
#
# Supervisors:
#   Dennis Schroers
#   Egshiglen Batbayar
#
# Date: 2026-02-21
#
# Usage:
#   - Run this script in R/RStudio.
#   - Required packages: data.table, ggplot2, parallel
#   - Outputs are written to: ./mc_out_fpy_vs_nss/
# ============================================================

suppressPackageStartupMessages({
  library(data.table)
  library(ggplot2)
  library(parallel)
})


# -----------------------
# 0) SETTINGS
# -----------------------
set.seed(1)

# Output folder
out_dir <- file.path(getwd(), "mc_out_fpy_vs_nss")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(out_dir, "figures"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(out_dir, "tables"),  showWarnings = FALSE, recursive = TRUE)

# Monte Carlo reps
B <- 250

# maturity grid (semiannual)
x_grid <- seq(0.5, 30, by = 0.5)
idx_y_rmse <- which(x_grid >= 1.0)
N <- length(x_grid)

# coupon bond universe
bond_maturities_years <- 1:30
coupon_rates <- c(0.00, 0.01, 0.02, 0.03, 0.04, 0.05)
coupon_freq <- 2
face <- 100
M <- length(bond_maturities_years) * length(coupon_rates)

# noise 
price_noise_sd_frac <- 0.05

# Cross-validation
K_folds <- 5

# KR hyperparameter grids
delta_grid  <- c(0.25, 0.50, 0.75)         
alpha_grid  <- c(0.05, 0.10, 0.25)         
lambda_grid <- 10^seq(-14, 0, by = 1)

# NSS tuning grids
kappa_grid <- 10^seq(-10, -2, by = 1)      
nss_start_grid <- c(8, 12, 20)
nss_maxit <- 6000

# Parallel (Mac/Linux: mclapply works; Windows: auto fallback)
use_parallel <- FALSE
n_cores <- max(1, parallel::detectCores() - 1)
is_windows <- (.Platform$OS.type == "windows")
if (is_windows) use_parallel <- FALSE

# Numerical guards
jitterK <- 1e-10
jitterA <- 1e-10
omega_floor <- 1e-8

g_floor <- 1e-8

y_cap <- 0.20  

# Store per-rep curves for band plots
store_curves <- TRUE

# -----------------------
# 1) TRUE CURVE
# -----------------------
true_y <- function(t) {
  0.020 +
    0.015 * (1 - exp(-t/2.0)) / (t/2.0) +
    0.010 * ((1 - exp(-t/5.0)) / (t/5.0) - exp(-t/5.0)) +
    0.006 * exp(-(t - 7)^2 / 8) -
    0.005 * exp(-(t - 18)^2 / 12)
}
y0_grid <- true_y(x_grid)
g0_grid <- exp(-x_grid * y0_grid)

# -----------------------
# 2) CASH-FLOW MATRIX C (M x N)
# -----------------------
map_to_grid_idx <- function(pay_times, x_grid, tol = 1e-12) {
  idx <- integer(length(pay_times))
  for (k in seq_along(pay_times)) {
    t <- pay_times[k]
    j <- which(abs(x_grid - t) < tol)
    if (length(j) >= 1) idx[k] <- j[1] else idx[k] <- which.min(abs(x_grid - t))
  }
  idx
}

build_cashflows <- function(x_grid, maturity_years, coupon_rate, coupon_freq = 2, face = 100) {
  pay_times <- seq(from = 1/coupon_freq, to = maturity_years, by = 1/coupon_freq)
  cpn_amt <- face * coupon_rate / coupon_freq
  cashflows <- rep(cpn_amt, length(pay_times))
  cashflows[length(cashflows)] <- cashflows[length(cashflows)] + face
  
  idx <- map_to_grid_idx(pay_times, x_grid)
  C_row <- numeric(length(x_grid))
  for (k in seq_along(idx)) C_row[idx[k]] <- C_row[idx[k]] + cashflows[k]
  C_row
}

bond_list <- vector("list", M)
k <- 0
for (m in bond_maturities_years) {
  for (c in coupon_rates) {
    k <- k + 1
    bond_list[[k]] <- list(maturity = m, coupon = c)
  }
}

C <- matrix(0, nrow = M, ncol = N)
for (i in seq_len(M)) {
  C[i, ] <- build_cashflows(x_grid, bond_list[[i]]$maturity, bond_list[[i]]$coupon, coupon_freq, face)
}

# Noise-free prices
P0 <- as.vector(C %*% g0_grid)
if (any(!is.finite(P0)) || any(P0 <= 0)) stop("Invalid noise-free prices; check setup.")
sigma <- price_noise_sd_frac * mean(P0)

# -----------------------
# 3) Utilities
# -----------------------
rmse <- function(a, b) sqrt(mean((a - b)^2, na.rm = TRUE))
rmse_bp <- function(a, b) 10000 * rmse(a, b)

to_yield <- function(g, x, g_floor_local = g_floor) {
  stopifnot(all(x > 0))
  g2 <- pmax(g, g_floor_local)
  -log(g2) / x
}

is_bad_yield_curve <- function(g, x, y_cap = y_cap) {
  y <- to_yield(g, x)
  any(!is.finite(y)) || any(y > y_cap)
}

# -----------------------
# 4) FPY Kernel bank 
# -----------------------
kernel_a0_d_in01 <- function(x, delta) {
  rho <- sqrt(delta / (1 - delta))
  Xmin <- outer(x, x, pmin)
  Xmax <- outer(x, x, pmax)
  (1/delta) * Xmin + (1/(2*delta*rho)) * (exp(-rho * (outer(x, x, "+"))) - exp(rho*Xmin - rho*Xmax))
}
kernel_a0_d1 <- function(x) outer(x, x, pmin)
kernel_ap_d1 <- function(x, alpha) {
  Xmin <- outer(x, x, pmin)
  (1/alpha) * (1 - exp(-alpha * Xmin))
}

stabilize_kernel <- function(K) {
  K <- 0.5 * (K + t(K))
  diag(K) <- diag(K) + jitterK
  K
}

make_kernel_bank <- function(x_grid, delta_grid, alpha_grid) {
  bank <- list()
  for (d in delta_grid) bank[[paste0("baseline_a0_din01_", d)]] <- stabilize_kernel(kernel_a0_d_in01(x_grid, d))
  bank[["robust_a0_d1"]] <- stabilize_kernel(kernel_a0_d1(x_grid))
  for (a in alpha_grid) bank[[paste0("robust_ap_d1_", a)]] <- stabilize_kernel(kernel_ap_d1(x_grid, a))
  bank
}
K_bank <- make_kernel_bank(x_grid, delta_grid, alpha_grid)

kernel_regime_from_name <- function(nm) {
  if (grepl("^baseline_a0_din01_", nm)) return("baseline_a0_din01")
  if (nm == "robust_a0_d1") return("robust_a0_d1")
  if (grepl("^robust_ap_d1_", nm)) return("robust_ap_d1")
  "other"
}

# -----------------------
# 5) FPY KR estimator
# -----------------------
estimate_kr <- function(C, K, omega_rep, lambda, P, g_base) {
  M <- nrow(C)
  
  Lambda <- diag(lambda / omega_rep, nrow = M)
  A <- C %*% K %*% t(C) + Lambda
  A <- 0.5 * (A + t(A))
  diag(A) <- diag(A) + jitterA
  
  rhs <- as.vector(P - (C %*% g_base))
  
  R <- chol(A)
  u <- backsolve(R, forwardsolve(t(R), rhs))
  beta <- as.vector(t(C) %*% u)
  
  ghat <- as.vector(g_base + K %*% beta)
  pmax(ghat, g_floor)
}

# -----------------------
# 6) NSS benchmark
# -----------------------
nss_yield <- function(t, theta) {
  b0 <- theta[1]; b1 <- theta[2]; b2 <- theta[3]; b3 <- theta[4]
  tau1 <- theta[5]; tau2 <- theta[6]
  x1 <- t / tau1
  x2 <- t / tau2
  f1 <- (1 - exp(-x1)) / pmax(x1, 1e-8)
  f2 <- f1 - exp(-x1)
  f3 <- (1 - exp(-x2)) / pmax(x2, 1e-8) - exp(-x2)
  b0 + b1 * f1 + b2 * f2 + b3 * f3
}
nss_discount <- function(t, theta) exp(-t * nss_yield(t, theta))

nss_objective <- function(theta, C, x_grid, P_obs, omega_rep, kappa = 0) {
  if (any(!is.finite(theta))) return(1e18)
  if (theta[5] <= 0.05 || theta[6] <= 0.05) return(1e18)
  g <- nss_discount(x_grid, theta)
  if (any(!is.finite(g)) || any(g <= 0)) return(1e18)
  P_hat <- as.vector(C %*% g)
  fit <- sum(omega_rep * (P_obs - P_hat)^2)
  pen <- kappa * sum(theta[2:4]^2)
  fit + pen
}

fit_nss <- function(C, x_grid, P_obs, omega_rep, n_starts = 12, maxit = 6000, kappa = 0) {
  lower <- c(-0.05, -0.25, -0.25, -0.25, 0.10, 0.10)
  upper <- c( 0.10,  0.25,  0.25,  0.25, 10.0, 10.0)
  
  best_val <- Inf
  best_par <- NULL
  for (s in seq_len(n_starts)) {
    theta0 <- runif(6, lower, upper)
    fit <- try(
      optim(theta0, nss_objective,
            C = C, x_grid = x_grid, P_obs = P_obs, omega_rep = omega_rep, kappa = kappa,
            method = "L-BFGS-B", lower = lower, upper = upper,
            control = list(maxit = maxit)),
      silent = TRUE
    )
    if (!inherits(fit, "try-error") && is.finite(fit$value) && fit$value < best_val) {
      best_val <- fit$value
      best_par <- fit$par
    }
  }
  if (is.null(best_par)) stop("NSS fit failed in all starts.")
  best_par
}

# -----------------------
# 7) CV folds + tuning
# -----------------------
make_folds <- function(M, K = 5, seed = 1) {
  set.seed(seed)
  id <- sample.int(M)
  split(id, rep(1:K, length.out = M))
}

cv_score_kr <- function(P_obs, C, omega_rep, Kmat, lambda, folds, g_base) {
  fold_rmse <- numeric(length(folds))
  for (k in seq_along(folds)) {
    idx_val <- folds[[k]]
    idx_tr  <- setdiff(seq_len(nrow(C)), idx_val)
    
    C_tr <- C[idx_tr, , drop = FALSE]
    C_v  <- C[idx_val, , drop = FALSE]
    P_tr <- P_obs[idx_tr]
    P_v  <- P_obs[idx_val]
    om_tr <- omega_rep[idx_tr]
    om_v  <- omega_rep[idx_val]
    
    ghat <- estimate_kr(C_tr, Kmat, om_tr, lambda, P_tr, g_base)
    P_hat_v <- as.vector(C_v %*% ghat)
    fold_rmse[k] <- sqrt(sum(om_v * (P_v - P_hat_v)^2) / sum(om_v))
  }
  mean(fold_rmse)
}

tune_kr_cv <- function(P_obs, C, omega_rep, K_bank, folds, lambda_grid, g_base,
                       use_parallel = TRUE, n_cores = 2) {
  grid <- CJ(kernel = names(K_bank), lambda = lambda_grid)
  
  eval_one <- function(i) {
    nm  <- grid$kernel[i]
    lam <- grid$lambda[i]
    sc  <- cv_score_kr(P_obs, C, omega_rep, K_bank[[nm]], lam, folds, g_base)
    data.table(kernel = nm, lambda = lam, cv_rmse = sc)
  }
  
  if (use_parallel && n_cores > 1) {
    res <- rbindlist(mclapply(seq_len(nrow(grid)), eval_one, mc.cores = n_cores))
  } else {
    res <- rbindlist(lapply(seq_len(nrow(grid)), eval_one))
  }
  setorder(res, cv_rmse)
  res[1]
}

cv_score_nss <- function(P_obs, C, omega_rep, x_grid, folds, kappa, n_starts) {
  fold_rmse <- numeric(length(folds))
  for (k in seq_along(folds)) {
    idx_val <- folds[[k]]
    idx_tr  <- setdiff(seq_len(nrow(C)), idx_val)
    
    C_tr <- C[idx_tr, , drop = FALSE]
    C_v  <- C[idx_val, , drop = FALSE]
    P_tr <- P_obs[idx_tr]
    P_v  <- P_obs[idx_val]
    om_tr <- omega_rep[idx_tr]
    om_v  <- omega_rep[idx_val]
    
    theta <- fit_nss(C_tr, x_grid, P_tr, om_tr, n_starts = n_starts, maxit = nss_maxit, kappa = kappa)
    ghat  <- pmax(nss_discount(x_grid, theta), g_floor)
    P_hat_v <- as.vector(C_v %*% ghat)
    
    fold_rmse[k] <- sqrt(sum(om_v * (P_v - P_hat_v)^2) / sum(om_v))
  }
  mean(fold_rmse)
}

tune_nss_cv <- function(P_obs, C, omega_rep, x_grid, folds, kappa_grid, nss_start_grid,
                        use_parallel = TRUE, n_cores = 2) {
  grid <- CJ(kappa = kappa_grid, n_starts = nss_start_grid)
  
  eval_one <- function(i) {
    kap <- grid$kappa[i]
    ns  <- grid$n_starts[i]
    sc  <- cv_score_nss(P_obs, C, omega_rep, x_grid, folds, kap, ns)
    data.table(kappa = kap, n_starts = ns, cv_rmse = sc)
  }
  
  if (use_parallel && n_cores > 1) {
    res <- rbindlist(mclapply(seq_len(nrow(grid)), eval_one, mc.cores = n_cores))
  } else {
    res <- rbindlist(lapply(seq_len(nrow(grid)), eval_one))
  }
  setorder(res, cv_rmse)
  res[1]
}

# -----------------------
# 8) MC storage containers
# -----------------------
if (store_curves) {
  yhat_KR_mat  <- matrix(NA_real_, nrow = B, ncol = N)
  yhat_NSS_mat <- matrix(NA_real_, nrow = B, ncol = N)
  ghat_KR_mat  <- matrix(NA_real_, nrow = B, ncol = N)
  ghat_NSS_mat <- matrix(NA_real_, nrow = B, ncol = N)
}

# -----------------------
# 9) One replication runner
# -----------------------
run_one_rep <- function(b) {
  P_obs <- P0 + rnorm(M, 0, sigma)
  
  y_base <- 0.03
  g_base <- exp(-x_grid * y_base)
  
  compute_duration <- function(C_row, x_grid, g_vec, P_i) {
    pv_cf <- C_row * g_vec
    sum(x_grid * pv_cf) / pmax(P_i, 1e-8)
  }
  
  D_base <- vapply(seq_len(M),
                   function(i) compute_duration(C[i, ], x_grid, g_base, sum(C[i, ] * g_base)),
                   numeric(1))
  
  omega_rep <- (1 / M) * 1 / (pmax(D_base * pmax(P_obs, 1e-8), 1e-8)^2)
  omega_rep <- pmax(omega_rep, omega_floor)
  
  folds <- make_folds(M, K = K_folds, seed = 1000 + b)
  
  best_kr <- tune_kr_cv(P_obs, C, omega_rep, K_bank, folds, lambda_grid,
                        g_base = g_base,
                        use_parallel = FALSE, n_cores = 1)
  
  g_kr <- estimate_kr(C, K_bank[[best_kr$kernel]], omega_rep, best_kr$lambda, P_obs, g_base)
  
  best_nss <- tune_nss_cv(P_obs, C, omega_rep, x_grid, folds, kappa_grid, nss_start_grid,
                          use_parallel = FALSE, n_cores = 1)
  
  theta <- fit_nss(C, x_grid, P_obs, omega_rep,
                   n_starts = best_nss$n_starts, maxit = nss_maxit, kappa = best_nss$kappa)
  
  g_nss <- pmax(nss_discount(x_grid, theta), g_floor)
  
  P_kr  <- as.vector(C %*% g_kr)
  P_nss <- as.vector(C %*% g_nss)
  
  y_kr  <- to_yield(g_kr,  x_grid)
  y_nss <- to_yield(g_nss, x_grid)
  
  bad_kr  <- is_bad_yield_curve(g_kr,  x_grid, y_cap = y_cap)
  bad_nss <- is_bad_yield_curve(g_nss, x_grid, y_cap = y_cap)
  
  kr_y_rmse_bp  <- if (!bad_kr)  rmse_bp(y_kr[idx_y_rmse],  y0_grid[idx_y_rmse]) else NA_real_
  nss_y_rmse_bp <- if (!bad_nss) rmse_bp(y_nss[idx_y_rmse], y0_grid[idx_y_rmse]) else NA_real_
  
  out_metrics <- data.table(
    rep = b,
    kr_kernel = best_kr$kernel,
    kr_kernel_regime = kernel_regime_from_name(best_kr$kernel),
    kr_lambda = best_kr$lambda,
    kr_cv_rmse = best_kr$cv_rmse,
    nss_kappa = best_nss$kappa,
    nss_nstarts = best_nss$n_starts,
    nss_cv_rmse = best_nss$cv_rmse,
    
    kr_price_rmse  = rmse(P_kr,  P0),
    nss_price_rmse = rmse(P_nss, P0),
    
    kr_yield_rmse_bp  = kr_y_rmse_bp,
    nss_yield_rmse_bp = nss_y_rmse_bp,
    
    kr_bad_curve  = as.integer(bad_kr),
    nss_bad_curve = as.integer(bad_nss),
    
    KR_beats_NSS_price    = as.integer(rmse(P_kr, P0) < rmse(P_nss, P0)),
    KR_beats_NSS_yield_bp = as.integer(!is.na(kr_y_rmse_bp) && !is.na(nss_y_rmse_bp) && (kr_y_rmse_bp < nss_y_rmse_bp))
  )
  
  if (store_curves) {
    list(metrics = out_metrics, y_kr = y_kr, y_nss = y_nss, g_kr = g_kr, g_nss = g_nss,
         P_obs = P_obs, P_kr = P_kr, P_nss = P_nss)
  } else {
    out_metrics
  }
}

# -----------------------
# 10) RUN MC
# -----------------------
cat("Running MC: B =", B, "| bonds M =", M, "| grid N =", N, "| folds =", K_folds,
    "| parallel =", use_parallel, "| cores =", n_cores, "\n")

if (use_parallel && n_cores > 1) {
  mc_list <- mclapply(seq_len(B), run_one_rep, mc.cores = n_cores)
} else {
  mc_list <- lapply(seq_len(B), run_one_rep)
}

if (store_curves) {
  mc_dt <- rbindlist(lapply(mc_list, `[[`, "metrics"))
  
  for (b in seq_len(B)) {
    yhat_KR_mat[b, ]  <- mc_list[[b]]$y_kr
    yhat_NSS_mat[b, ] <- mc_list[[b]]$y_nss
    ghat_KR_mat[b, ]  <- mc_list[[b]]$g_kr
    ghat_NSS_mat[b, ] <- mc_list[[b]]$g_nss
  }
  
  saveRDS(list(
    x_grid = x_grid,
    y0_grid = y0_grid,
    g0_grid = g0_grid,
    yhat_KR_mat = yhat_KR_mat,
    yhat_NSS_mat = yhat_NSS_mat,
    ghat_KR_mat = ghat_KR_mat,
    ghat_NSS_mat = ghat_NSS_mat
  ), file.path(out_dir, "mc_curves.rds"))
  
  saveRDS(list(
    P0 = P0,
    P_obs = mc_list[[1]]$P_obs,
    P_kr = mc_list[[1]]$P_kr,
    P_nss = mc_list[[1]]$P_nss
  ), file.path(out_dir, "rep1_prices.rds"))
} else {
  mc_dt <- rbindlist(mc_list)
}

fwrite(mc_dt, file.path(out_dir, "mc_results.csv"))

# -----------------------
# 11) TABLES (robust summaries + fail rates)
# -----------------------
summ_stats <- function(x) {
  x <- x[is.finite(x)]
  if (length(x) == 0) return(c(mean=NA, median=NA, sd=NA, p10=NA, p90=NA))
  c(
    mean   = mean(x),
    median = median(x),
    sd     = sd(x),
    p10    = as.numeric(quantile(x, 0.10)),
    p90    = as.numeric(quantile(x, 0.90))
  )
}

tbl_rmse <- rbind(
  data.table(model="KR",  metric="Price RMSE",        t(summ_stats(mc_dt$kr_price_rmse))),
  data.table(model="NSS", metric="Price RMSE",        t(summ_stats(mc_dt$nss_price_rmse))),
  data.table(model="KR",  metric="Yield RMSE (bp)",   t(summ_stats(mc_dt$kr_yield_rmse_bp))),
  data.table(model="NSS", metric="Yield RMSE (bp)",   t(summ_stats(mc_dt$nss_yield_rmse_bp)))
)
fwrite(tbl_rmse, file.path(out_dir, "tables", "summary_rmse.csv"))

# Win rates:
# - Price win rate always defined
# - Yield win rate computed only for reps where both yield RMSE are non-NA
yield_ok <- is.finite(mc_dt$kr_yield_rmse_bp) & is.finite(mc_dt$nss_yield_rmse_bp)

win_tbl <- data.table(
  B = B,
  
  win_rate_price = mean(mc_dt$KR_beats_NSS_price),
  
  yield_comparable_share = mean(yield_ok),
  win_rate_yield_bp = if (any(yield_ok)) mean(mc_dt$KR_beats_NSS_yield_bp[yield_ok]) else NA_real_,
  
  fail_rate_kr  = mean(mc_dt$kr_bad_curve == 1),
  fail_rate_nss = mean(mc_dt$nss_bad_curve == 1),
  
  mean_price_rmse_KR  = mean(mc_dt$kr_price_rmse),
  mean_price_rmse_NSS = mean(mc_dt$nss_price_rmse),
  
  mean_yield_rmse_bp_KR  = mean(mc_dt$kr_yield_rmse_bp,  na.rm = TRUE),
  mean_yield_rmse_bp_NSS = mean(mc_dt$nss_yield_rmse_bp, na.rm = TRUE),
  
  median_yield_rmse_bp_KR  = median(mc_dt$kr_yield_rmse_bp,  na.rm = TRUE),
  median_yield_rmse_bp_NSS = median(mc_dt$nss_yield_rmse_bp, na.rm = TRUE)
)
fwrite(win_tbl, file.path(out_dir, "tables", "win_rates.csv"))


# -----------------------
# 12) DONE
# -----------------------
cat("\nSaved outputs to:\n", out_dir, "\n")
cat(" - mc_results.csv\n - mc_curves.rds\n - rep1_prices.rds\n")
cat(" - tables/summary_rmse.csv\n - tables/win_rates.csv\n\n")

cat("Win rates:\n")
cat("  KR beats NSS (price):", round(mean(mc_dt$KR_beats_NSS_price), 3), "\n")
cat("  Yield comparable share:", round(mean(yield_ok), 3), "\n")
cat("  KR beats NSS (yield, bp | comparable only):",
    if (any(yield_ok)) round(mean(mc_dt$KR_beats_NSS_yield_bp[yield_ok]), 3) else NA, "\n")
cat("  Fail rates (KR/NSS):", round(mean(mc_dt$kr_bad_curve==1),3), "/", round(mean(mc_dt$nss_bad_curve==1),3), "\n")
