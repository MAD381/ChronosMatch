"""
CHRONOSMATCH - MODULE 8
AI PORTFOLIO OPTIMIZER

Purpose:
1. Collect historical stock prices.
2. Calculate daily stock returns.
3. Calculate risk and expected return.
4. Generate different portfolio allocations.
5. Find the allocation with the best Sharpe ratio.
6. Display the recommended sample allocation.

Educational project only. It does not place trades.
"""

import numpy as np
import pandas as pd
import yfinance as yf

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]

PERIOD = "1y"
NUMBER_OF_PORTFOLIOS = 10000

# Illustrative annual risk-free rate
RISK_FREE_RATE = 0.06


# --------------------------------------------------
# STEP 1: COLLECT STOCK DATA
# --------------------------------------------------


def collect_stock_data():

    print("\nSTEP 1: COLLECTING STOCK DATA")
    print("-" * 50)

    data = yf.download(
        STOCKS, period=PERIOD, interval="1d", auto_adjust=True, progress=False
    )

    if data.empty:
        raise RuntimeError("Unable to download stock data. Check internet connection.")

    if isinstance(data.columns, pd.MultiIndex):
        if "Close" in data.columns.get_level_values(0):
            prices = data["Close"]
        else:
            prices = data.xs("Close", axis=1, level=1)
    else:
        prices = data[["Close"]].rename(columns={"Close": STOCKS[0]})

    prices = prices.dropna(axis=1, how="all")
    prices = prices.ffill().dropna()

    if prices.shape[1] < 2 or len(prices) < 30:
        raise RuntimeError("Not enough historical data for portfolio optimization.")

    print("Stocks downloaded successfully.")

    print("\nAvailable stocks:")
    for stock in prices.columns:
        print("-", stock)

    print("\nHistorical records:", len(prices))

    return prices


# --------------------------------------------------
# STEP 2: CALCULATE STOCK RETURNS
# --------------------------------------------------


def calculate_returns(prices):

    print("\nSTEP 2: CALCULATING STOCK RETURNS")
    print("-" * 50)

    daily_returns = prices.pct_change().dropna()

    average_returns = daily_returns.mean() * 252

    print("\nAnnualized historical returns:")

    for stock, value in average_returns.items():
        print(f"{stock}: {value * 100:.2f}%")

    return daily_returns


# --------------------------------------------------
# STEP 3: GENERATE PORTFOLIO ALLOCATIONS
# --------------------------------------------------


def generate_portfolios(returns):

    print("\nSTEP 3: GENERATING PORTFOLIOS")
    print("-" * 50)

    number_of_stocks = len(returns.columns)

    average_returns = returns.mean() * 252

    covariance = returns.cov() * 252

    # Random long-only allocations.
    # Every portfolio's weights add up to 100%.
    rng = np.random.default_rng(42)

    weights = rng.dirichlet(np.ones(number_of_stocks), size=NUMBER_OF_PORTFOLIOS)

    portfolio_returns = weights @ average_returns.to_numpy()

    portfolio_variances = np.einsum(
        "ij,jk,ik->i", weights, covariance.to_numpy(), weights
    )

    portfolio_risks = np.sqrt(np.maximum(portfolio_variances, 0))

    sharpe_ratios = np.divide(
        portfolio_returns - RISK_FREE_RATE,
        portfolio_risks,
        out=np.full_like(portfolio_returns, -np.inf),
        where=portfolio_risks > 0,
    )

    print(f"Generated {NUMBER_OF_PORTFOLIOS:,} " "possible portfolio allocations.")

    return (weights, portfolio_returns, portfolio_risks, sharpe_ratios)


# --------------------------------------------------
# STEP 4: FIND OPTIMAL PORTFOLIO
# --------------------------------------------------


def find_optimal_portfolio(weights, returns, risks, sharpe_ratios):

    print("\nSTEP 4: FINDING OPTIMAL PORTFOLIO")
    print("-" * 50)

    best_index = int(np.argmax(sharpe_ratios))

    best_weights = weights[best_index]

    best_return = returns[best_index]

    best_risk = risks[best_index]

    best_sharpe = sharpe_ratios[best_index]

    return (best_weights, best_return, best_risk, best_sharpe)


# --------------------------------------------------
# STEP 5: DISPLAY RESULTS
# --------------------------------------------------


def display_results(stocks, weights, expected_return, risk, sharpe):

    print("\nSTEP 5: OPTIMIZED PORTFOLIO RESULTS")
    print("=" * 60)

    print("\nSuggested sample allocation:")

    for stock, weight in zip(stocks, weights):

        print(f"{stock:<15}: {weight * 100:6.2f}%")

    print("\nPORTFOLIO PERFORMANCE")
    print("-" * 50)

    print(f"Historical annualized return: " f"{expected_return * 100:.2f}%")

    print(f"Historical annualized risk: " f"{risk * 100:.2f}%")

    print(f"Sharpe ratio: {sharpe:.3f}")

    print("\nPASS: Portfolio optimization completed.")

    print(
        "\nNote: These are historical estimates, "
        "not guaranteed future returns or financial advice."
    )


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------


def main():

    print("=" * 60)
    print("CHRONOSMATCH - AI PORTFOLIO OPTIMIZER")
    print("MODULE 8")
    print("=" * 60)

    try:

        # Step 1
        prices = collect_stock_data()

        # Step 2
        returns = calculate_returns(prices)

        # Step 3
        weights, portfolio_returns, portfolio_risks, sharpe_ratios = (
            generate_portfolios(returns)
        )

        # Step 4
        best_weights, best_return, best_risk, best_sharpe = find_optimal_portfolio(
            weights, portfolio_returns, portfolio_risks, sharpe_ratios
        )

        # Step 5
        display_results(
            returns.columns, best_weights, best_return, best_risk, best_sharpe
        )

        return True

    except Exception as error:

        print("\nMODULE 8 ERROR:", error)

        return False


# --------------------------------------------------
# PROGRAM EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    success = main()

    if not success:
        raise SystemExit(1)
