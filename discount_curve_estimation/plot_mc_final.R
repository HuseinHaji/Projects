# ============================================================
# Discount Curve Estimation from Coupon Bonds:
# A Monte Carlo Assessment of Smoothness Regularization
#
# Companion script (Post-processing):
#   - Reads saved Monte Carlo outputs from ./mc_out_fpy_vs_nss/
#   - Produces summary figures (bands, errors, price-fit) and tables
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
# Inputs expected (created by the MC runner script):
#   - mc_out_fpy_vs_nss/mc_results.csv
#   - mc_out_fpy_vs_nss/mc_curves.rds
#   - mc_out_fpy_vs_nss/rep1_prices.rds (optional)
#
# Outputs written to:
#   - mc_out_fpy_vs_nss/figures_summary/
#   - mc_out_fpy_vs_nss/tables_summary/
# ============================================================

suppressPackageStartupMessages({
  library(data.table)
  library(ggplot2)
  library(scales)
})

# -----------------------
# 0) SET PATHS
# -----------------------
out_dir <- file.path(getwd(), "mc_out_fpy_vs_nss")

fig_dir <- file.path(out_dir, "figures_summary")
dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)

# -----------------------
# 1) Robust file locator
# -----------------------
find_file <- function(relpath) {
  cand <- c(
    file.path(out_dir, relpath),
    file.path(getwd(), relpath),
    file.path(getwd(), "mc_out_fpy_vs_nss", relpath),
    file.path("/mnt/data", relpath)
  )
  hit <- cand[file.exists(cand)][1]
  if (is.na(hit)) stop("Missing file: ", relpath, "\nTried:\n", paste(cand, collapse = "\n"))
  hit
}

path_mc   <- find_file("mc_results.csv")
path_curv <- find_file("mc_curves.rds")
path_rep1 <- try(find_file("rep1_prices.rds"), silent = TRUE)

mc_dt  <- fread(path_mc)
curves <- readRDS(path_curv)

xg <- curves$x_grid
y0 <- curves$y0_grid
g0 <- curves$g0_grid

yKR  <- curves$yhat_KR_mat
gKR  <- curves$ghat_KR_mat
yNSS <- curves$yhat_NSS_mat
gNSS <- curves$ghat_NSS_mat

B_eff <- nrow(yKR)

# -----------------------
# 2) Plot theme
# -----------------------
theme_pub <- theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 20, hjust = 0),
    panel.grid.minor = element_blank(),
    legend.position = "bottom",
    plot.caption = element_text(size = 11, hjust = 0)
  )

# -----------------------
# 3) Helpers: pointwise bands
# -----------------------
bands_dt <- function(mat, x) {
  stopifnot(ncol(mat) == length(x))
  data.table(
    x   = x,
    q05 = apply(mat, 2, quantile, probs = 0.05, na.rm = TRUE),
    q25 = apply(mat, 2, quantile, probs = 0.25, na.rm = TRUE),
    q50 = apply(mat, 2, quantile, probs = 0.50, na.rm = TRUE),
    q75 = apply(mat, 2, quantile, probs = 0.75, na.rm = TRUE),
    q95 = apply(mat, 2, quantile, probs = 0.95, na.rm = TRUE)
  )
}

# ============================================================
# FIG 1) Curve recovery (Yield): KR vs NSS vs Truth (bands)
# ============================================================
df_y_kr  <- bands_dt(yKR, xg)[, model := "KR"]
df_y_nss <- bands_dt(yNSS, xg)[, model := "NSS"]
df_y <- rbind(df_y_kr, df_y_nss)
df_truth_y <- data.table(x = xg, y0 = y0)

p1 <- ggplot(df_y, aes(x = x)) +
  geom_ribbon(aes(ymin = q05, ymax = q95, fill = model), alpha = 0.12) +
  geom_ribbon(aes(ymin = q25, ymax = q75, fill = model), alpha = 0.22) +
  geom_line(aes(y = q50, color = model), linewidth = 1.1) +
  geom_line(data = df_truth_y, aes(y = y0), linetype = "dashed", linewidth = 1.1) +
  labs(
    title = "MC Curve Recovery: Yield (Truth vs KR vs NSS)",
    x = "Maturity (years)", y = "Zero-coupon yield",
    caption = sprintf("Pointwise bands across B = %d replications. Dashed line = true y0(t).", B_eff)
  ) +
  theme_pub
ggsave(file.path(fig_dir, "P1_yield_recovery_KR_vs_NSS.png"), p1, width = 12.5, height = 7.2, dpi = 220)

# ============================================================
# FIG 2) Identification map (Yield error by maturity): KR vs NSS
# ============================================================
errKR  <- sweep(yKR,  2, y0, FUN = "-")
errNSS <- sweep(yNSS, 2, y0, FUN = "-")

df_e_kr  <- bands_dt(errKR, xg)[, model := "KR"]
df_e_nss <- bands_dt(errNSS, xg)[, model := "NSS"]
df_e <- rbind(df_e_kr, df_e_nss)

p2 <- ggplot(df_e, aes(x = x)) +
  geom_hline(yintercept = 0, linetype = "dashed", linewidth = 1.0) +
  geom_ribbon(aes(ymin = q05, ymax = q95, fill = model), alpha = 0.12) +
  geom_ribbon(aes(ymin = q25, ymax = q75, fill = model), alpha = 0.22) +
  geom_line(aes(y = q50, color = model), linewidth = 1.1) +
  labs(
    title = "MC Identification Map: Yield Error by Maturity",
    x = "Maturity (years)", y = "Error (ŷ(t) − y0(t))",
    caption = "Dashed horizontal line is zero error. Wider bands = weaker identification at that maturity."
  ) +
  theme_pub
ggsave(file.path(fig_dir, "P2_yield_error_by_maturity.png"), p2, width = 12.5, height = 7.2, dpi = 220)

# ============================================================
# FIG 3) Discount recovery: KR vs NSS vs Truth (bands)
# ============================================================
df_g_kr  <- bands_dt(gKR, xg)[, model := "KR"]
df_g_nss <- bands_dt(gNSS, xg)[, model := "NSS"]
df_g <- rbind(df_g_kr, df_g_nss)
df_truth_g <- data.table(x = xg, g0 = g0)

p3 <- ggplot(df_g, aes(x = x)) +
  geom_ribbon(aes(ymin = q05, ymax = q95, fill = model), alpha = 0.12) +
  geom_ribbon(aes(ymin = q25, ymax = q75, fill = model), alpha = 0.22) +
  geom_line(aes(y = q50, color = model), linewidth = 1.1) +
  geom_line(data = df_truth_g, aes(y = g0), linetype = "dashed", linewidth = 1.1) +
  labs(
    title = "MC Curve Recovery: Discount Factor (Truth vs KR vs NSS)",
    x = "Maturity (years)", y = "Discount factor g(t)",
    caption = "Dashed line = true g0(t). Discount-factor recovery is the pricing-relevant object."
  ) +
  theme_pub
ggsave(file.path(fig_dir, "P3_discount_recovery_KR_vs_NSS.png"), p3, width = 12.5, height = 7.2, dpi = 220)

# ============================================================
# FIG 4) One-replication price fit (observed vs fitted; KR and NSS)
# ============================================================
if (!inherits(path_rep1, "try-error")) {
  rep1 <- readRDS(path_rep1)
  df_pf <- rbind(
    data.table(model = "KR",  P_obs = rep1$P_obs, P_fit = rep1$P_kr),
    data.table(model = "NSS", P_obs = rep1$P_obs, P_fit = rep1$P_nss)
  )
  lims <- range(c(df_pf$P_obs, df_pf$P_fit), finite = TRUE)
  
  p6 <- ggplot(df_pf, aes(x = P_obs, y = P_fit)) +
    geom_point(alpha = 0.55, size = 1.8) +
    geom_abline(intercept = 0, slope = 1, linetype = "dashed", linewidth = 1.1) +
    facet_wrap(~model, scales = "fixed") +
    coord_equal(xlim = lims, ylim = lims) +
    labs(
      title = "One Replication: Observed Prices vs Fitted Prices",
      x = "Observed noisy price P_obs", y = "Model-implied price",
      caption = "Dashed 45° line is perfect fit. This is the most intuitive pricing diagnostic."
    ) +
    theme_pub
  ggsave(file.path(fig_dir, "P6_rep1_price_fit_KR_vs_NSS.png"), p6, width = 12.5, height = 6.8, dpi = 220)
}

# ============================================================
# MONTE CARLO TABLES
# ============================================================
suppressPackageStartupMessages({
  library(data.table)
})

out_dir <- file.path(getwd(), "mc_out_fpy_vs_nss")
tab_dir <- file.path(out_dir, "tables_summary")
dir.create(tab_dir, showWarnings = FALSE, recursive = TRUE)

mc_path   <- file.path(out_dir, "mc_results.csv")
rep1_path <- file.path(out_dir, "rep1_prices.rds")

mc_dt <- fread(mc_path)

# ============================================================
# TABLE 1: RMSE SUMMARY STATISTICS
# ============================================================
summ_stats <- function(x) {
  x <- x[is.finite(x)]  # drops NA, NaN, Inf, -Inf
  if (length(x) == 0L) {
    return(c(mean = NA_real_, median = NA_real_, sd = NA_real_, q10 = NA_real_, q90 = NA_real_))
  }
  c(
    mean   = mean(x),
    median = median(x),
    sd     = sd(x),
    q10    = as.numeric(quantile(x, 0.10, na.rm = TRUE, names = FALSE)),
    q90    = as.numeric(quantile(x, 0.90, na.rm = TRUE, names = FALSE))
  )
}

tbl_rmse <- rbind(
  data.table(model = "FPY (KR)", metric = "Pricing RMSE",
             t(summ_stats(mc_dt$kr_price_rmse))),
  data.table(model = "NSS", metric = "Pricing RMSE",
             t(summ_stats(mc_dt$nss_price_rmse))),
  data.table(model = "FPY (KR)", metric = "Yield RMSE",
             t(summ_stats(mc_dt$kr_yield_rmse_bp))),
  data.table(model = "NSS", metric = "Yield RMSE",
             t(summ_stats(mc_dt$nss_yield_rmse_bp)))
)

fwrite(tbl_rmse, file.path(tab_dir, "Table1_RMSE_summary.csv"))

# ============================================================
# ONE TABLE PLOT (PNG)
# ============================================================
suppressPackageStartupMessages({
  library(data.table)
  library(ggplot2)
})

out_dir  <- file.path(getwd(), "mc_out_fpy_vs_nss")
mc_path  <- file.path(out_dir, "mc_results.csv")

stopifnot(file.exists(mc_path))

plot_dir <- file.path(out_dir, "tables_summary", "plots")
dir.create(plot_dir, showWarnings = FALSE, recursive = TRUE)

mc_dt <- fread(mc_path)

# -----------------------
# 1) (RMSE summary)
# -----------------------
summ_stats <- function(x) {
  c(
    Mean   = mean(x, na.rm = TRUE),
    Median = median(x, na.rm = TRUE),
    SD     = sd(x, na.rm = TRUE),
    P10    = as.numeric(quantile(x, 0.10, na.rm = TRUE)),
    P90    = as.numeric(quantile(x, 0.90, na.rm = TRUE))
  )
}

tbl <- rbind(
  data.table(Model="FPY (KR)", Metric="Pricing RMSE", t(summ_stats(mc_dt$kr_price_rmse))),
  data.table(Model="NSS",      Metric="Pricing RMSE", t(summ_stats(mc_dt$nss_price_rmse))),
  data.table(Model="FPY (KR)", Metric="Yield RMSE",   t(summ_stats(mc_dt$kr_yield_rmse_bp))),
  data.table(Model="NSS",      Metric="Yield RMSE",   t(summ_stats(mc_dt$nss_yield_rmse_bp)))
)

num_cols <- setdiff(names(tbl), c("Model","Metric"))
tbl[, (num_cols) := lapply(.SD, function(z) sprintf("%.6f", z)), .SDcols = num_cols]

# -----------------------
# 2) "table plot" with ggplot 
# -----------------------
make_table_plot <- function(dt, title, subtitle = NULL,
                            col_widths = NULL, row_height = 0.95,
                            header_fill = "grey12",
                            stripe_fill = "grey96",
                            border_col  = "grey80") {
  
  dt_plot <- copy(dt)
  
  cols <- names(dt_plot)
  
  if (is.null(col_widths)) {
    col_widths <- rep(1, length(cols))
    col_widths[1] <- 1.35
    if (length(cols) >= 2) col_widths[2] <- 1.55
  }
  stopifnot(length(col_widths) == length(cols))
  
  x_left <- c(0, cumsum(col_widths)[-length(col_widths)])
  x_mid  <- x_left + col_widths/2
  x_right <- x_left + col_widths
  x_total <- sum(col_widths)
  
  long <- rbindlist(lapply(seq_along(cols), function(j){
    data.table(
      row = seq_len(nrow(dt_plot)),
      col = cols[j],
      val = as.character(dt_plot[[j]]),
      j   = j
    )
  }))
  
  long[, stripe := as.integer(row %% 2 == 0)]
  
  bg_body <- unique(long[, .(row, stripe)])
  bg_body[, y0 := row - row_height/2]
  bg_body[, y1 := row + row_height/2]
  bg_body[, x0 := 0]
  bg_body[, x1 := x_total]
  
  cell_rect <- rbindlist(lapply(seq_along(cols), function(j){
    data.table(
      row = seq_len(nrow(dt_plot)),
      j = j,
      x0 = x_left[j],
      x1 = x_right[j],
      y0 = seq_len(nrow(dt_plot)) - row_height/2,
      y1 = seq_len(nrow(dt_plot)) + row_height/2
    )
  }))
  
  header_rect <- data.table(
    j = seq_along(cols),
    x0 = x_left,
    x1 = x_right,
    y0 = 0.15,
    y1 = 1.15
  )
  
  header_text <- data.table(
    j = seq_along(cols),
    label = cols,
    x = x_mid,
    y = 0.65
  )
  
  long[, x := x_mid[j]]
  long[, y := row]
  
  long[, hjust := ifelse(j <= 2, 0, 1)]
  long[, x_text := ifelse(j <= 2, x_left[j] + 0.08*col_widths[j], x_right[j] - 0.08*col_widths[j])]
  
  header_text[, x := x_mid]
  
  nrows <- nrow(dt_plot)
  
  p <- ggplot() +
    # title
    annotate("text", x = 0, y = -0.55, label = title, hjust = 0,
             fontface = "bold", size = 6) +
    { if (!is.null(subtitle))
      annotate("text", x = 0, y = -0.15, label = subtitle, hjust = 0,
               size = 4)
      else NULL } +
    
    # header background
    geom_rect(data = header_rect,
              aes(xmin = x0, xmax = x1, ymin = y0 - 1, ymax = y1 - 1),
              fill = header_fill, color = NA) +
    
    # body striping
    geom_rect(data = bg_body,
              aes(xmin = x0, xmax = x1, ymin = y0, ymax = y1),
              fill = stripe_fill, color = NA, inherit.aes = FALSE) +
    
    # grid borders (cells)
    geom_rect(data = cell_rect,
              aes(xmin = x0, xmax = x1, ymin = y0, ymax = y1),
              fill = NA, color = border_col, linewidth = 0.35) +
    
    # header borders
    geom_rect(data = header_rect,
              aes(xmin = x0, xmax = x1, ymin = y0 - 1, ymax = y1 - 1),
              fill = NA, color = border_col, linewidth = 0.6) +
    
    # header text
    geom_text(data = header_text,
              aes(x = x, y = y - 1, label = label),
              color = "white", fontface = "bold", size = 4.2) +
    
    # body text
    geom_text(data = long,
              aes(x = x_text, y = y, label = val, hjust = hjust),
              color = "grey10", size = 4.0) +
    
    # layout
    scale_x_continuous(limits = c(0, x_total), expand = c(0, 0)) +
    scale_y_reverse(limits = c(nrows + 0.7, -1.0), expand = c(0, 0)) +
    coord_cartesian(clip = "off") +
    theme_void() +
    theme(plot.margin = margin(12, 18, 12, 18))
  
  p
}

p_tbl <- make_table_plot(
  tbl,
  title = "Table: Monte Carlo RMSE Summary (FPY vs NSS)",
  subtitle = sprintf("B = %d replications. Numbers are mean / median / sd / 10th / 90th percentiles.", nrow(mc_dt)),
  col_widths = c(1.35, 1.70, 1.05, 1.05, 1.05, 1.05, 1.05)  # tweak if needed
)

out_file <- file.path(plot_dir, "Table_RMSE_Summary.png")
ggsave(out_file, p_tbl, width = 13.5, height = 3.8, dpi = 300)
