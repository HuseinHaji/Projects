# Market Stress Early-Warning System

[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-green)](https://pytest.org/)
[![Workflow](https://img.shields.io/badge/workflow-pytask-orange)](https://pytask-dev.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](#license)

**Detecting High-Volatility Regimes in Equity Markets Using Machine Learning**

## Overview

Financial markets periodically enter periods of elevated volatility and uncertainty.
Early detection of such regimes is critical for risk management and improving empirical
analysis of financial stress.

This project builds a **fully reproducible early-warning system** that predicts market
stress in the S&P 500 using volatility-based indicators and logistic regression. The
entire workflow is automated using `pytask` with comprehensive testing via `pytest`.

## Research Question

**Can simple volatility-based indicators effectively predict whether the market will
enter a high-volatility stress regime?**

## Key Features

**Reproducible Pipeline** – Automated workflow using `pytask` **Comprehensive Testing**
– Full test suite with `pytest` **Data-Driven Analysis** – Real-time expanding-window
backtesting **Publication-Ready Outputs** – Figures, tables, and visualizations
**Version-Controlled Environment** – Managed dependencies via Pixi

## Quick Start

### Prerequisites

- Python 3.14+
- [Pixi](https://pixi.sh/) for environment management

### Installation & Execution

```bash
# Clone the repository
git clone <repo-url>
cd final-project-HuseinHaji

# Install dependencies
pixi install

# Run the complete pipeline
pixi run pytask
```

All outputs will be generated in the `bld/` folder.

## Usage

### Run the Full Pipeline

```bash
pixi run pytask
```

This automatically:

- Downloads S&P 500 historical data
- Cleans and validates the dataset
- Constructs volatility-based features
- Trains the logistic regression model
- Runs an expanding-window backtest
- Generates figures and tables for publication

### Run Tests

```bash
pixi run pytest
```

### View Outputs

```bash
# View the research paper
pixi run view-paper

# View the presentation
pixi run view-pres
```

Validates:

- Data cleaning logic
- Feature construction
- Threshold computation without data leakage
- Model training procedures
- Backtest outputs
- Artifact generation

## Project Structure

```
final-project-HuseinHaji/
│
├── src/stress_prediction/
│   ├── utils/                 # Core functions (cleaning, features, models)
│   ├── analysis/              # Analysis tasks
│   ├── data_management/       # Data Management tasks
│   ├── final/                 # Final tasks
│   └── __init__.py
│
├── tests/                     # Automated test suite
│   └── test_*.py
│
├── documents/                 # Research paper and presentation sources
│
├── bld/                       # Generated outputs (figures, tables, data, models)
│   ├── figures/
│   ├── tables/
│   └── data/
│   └── models/
│
├── pyproject.toml             # Project metadata and dependencies
├── pixi.toml                  # Environment specification
├── README.md                  # This file
└── .gitignore
```

## Methodology

The pipeline implements a structured 7-step workflow:

### 1. **Data Download**

Retrieves daily S&P 500 price data from Stooq.

### 2. **Data Cleaning**

- Renames and standardizes columns
- Converts data types
- Ensures chronological ordering
- Validates data integrity

### 3. **Feature Construction**

- Lagged returns
- Lagged volatility measures
- Rolling window statistics

### 4. **Stress Regime Definition**

Volatility threshold computed from training data to classify stress periods.

### 5. **Model Training**

Logistic regression model trained to predict stress regime entry probability.

### 6. **Backtesting**

Expanding-window backtest simulates real-time forecasting performance without lookahead
bias.

### 7. **Artifact Generation**

Exports publication-ready figures, tables, and analysis results.

## Example Outputs

The pipeline generates:

- **ROC Curves** – Model discrimination performance
- **Probability Plots** – Predicted stress probabilities over time
- **Volatility Analysis** – Realized vs. predicted stress regimes
- **Performance Tables** – Model diagnostics and metrics

All outputs are saved in `bld/` and ready for publication.

## Reproducibility

This project adheres to reproducible research best practices:

- **Deterministic Pipeline** – `pytask` ensures consistent execution
- **Automated Testing** – `pytest` validates all components
- **Code Quality** – `pre-commit` hooks enforce standards
- **Version Control** – Dependencies locked in `pixi.toml`
- **Documentation** – Clear methodology and code comments

**Simply run `pixi run pytask` to reproduce the entire analysis from scratch.**

## Configuration

Edit `pyproject.toml` to customize:

- Data source and date ranges
- Feature parameters
- Model hyperparameters
- Backtest window sizes

## Dependencies

Core libraries:

- **pandas** – Data manipulation
- **scikit-learn** – Machine learning models
- **numpy** – Numerical computing
- **matplotlib/seaborn** – Visualization
- **pytask** – Workflow automation

See `pixi.toml` for complete environment specification.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
1. Create a feature branch
1. Add tests for new functionality
1. Submit a pull request

## License

This project is licensed under the MIT License – see `LICENSE` file for details.

## Acknowledgments

Project template inspired by
[Open Source Economics](https://github.com/OpenSourceEconomics/econ-project-templates)

## Author

**Huseyn Hajiyev**

- [![GitHub](https://img.shields.io/badge/GitHub-HuseinHaji-black?logo=github)](https://github.com/HuseinHaji)
- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Huseyn%20Hajiyev-blue?logo=linkedin)](https://www.linkedin.com/in/huseynhajiyev10/)

______________________________________________________________________

**Questions?** Open an issue on GitHub or contact the author directly.
