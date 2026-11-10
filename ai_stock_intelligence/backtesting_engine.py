"""
CHRONOSMATCH - MODULE 10
AI TRADING STRATEGY BACKTESTING ENGINE

Features:
1. Download historical stock data.
2. Calculate SMA 20 and SMA 50.
3. Generate trading positions.
4. Simulate historical strategy returns.
5. Include estimated transaction costs.
6. Calculate total return, volatility, Sharpe ratio
   and maximum drawdown.
7. Compare strategy performance with buy-and-hold.

Educational backtesting only. No real trades are placed.
"""

import numpy as np
import pandas as pd
import yfinance as yf

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

STOCK = "RELIANCE.NS"
PERIOD = "2y"

TRANSACTION_COST = 0.001  # 0.10% per position change


# --------------------------------------------------
# STEP 1: COLLECT HISTORICAL DATA
# --------------------------------------------------


def collect_data():

    print("\nSTEP 1: COLLECTING HISTORICAL DATA")
    print("-" * 55)

    data = yf.download(
        STOCK, period=PERIOD, interval="1d", auto_adjust=True, progress=False
    )

    if data.empty:
        raise RuntimeError("Historical stock data unavailable.")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if "Close" not in data.columns:
        raise RuntimeError("Closing price column is missing.")

    data = data[["Close"]].dropna().copy()

    if len(data) < 60:
        raise RuntimeError("Not enough historical data for backtesting.")

    print("Historical data downloaded successfully.")
    print("Total records:", len(data))

    return data


# --------------------------------------------------
# STEP 2: CALCULATE MOVING AVERAGES
# --------------------------------------------------


def calculate_indicators(data):

    print("\nSTEP 2: CALCULATING MOVING AVERAGES")
    print("-" * 55)

    data["SMA20"] = data["Close"].rolling(window=20).mean()

    data["SMA50"] = data["Close"].rolling(window=50).mean()

    print("SMA 20 calculated.")
    print("SMA 50 calculated.")

    return data


# --------------------------------------------------
# STEP 3: GENERATE STRATEGY POSITIONS
# --------------------------------------------------


def generate_positions(data):

    print("\nSTEP 3: GENERATING STRATEGY POSITIONS")
    print("-" * 55)

    # Position 1 means invested in the stock.
    # Position 0 means holding cash.
    data["Position"] = (data["SMA20"] > data["SMA50"]).astype(float)

    print("Moving-average trading positions generated.")

    return data


# --------------------------------------------------
# STEP 4: SIMULATE STRATEGY RETURNS
# --------------------------------------------------


def calculate_strategy_returns(data):

    print("\nSTEP 4: SIMULATING STRATEGY RETURNS")
    print("-" * 55)

    data["MarketReturn"] = data["Close"].pct_change().fillna(0)

    # Apply today's position to the next trading day's return.
    data["PreviousPosition"] = data["Position"].shift(1).fillna(0)

    data["StrategyReturnBeforeCost"] = data["PreviousPosition"] * data["MarketReturn"]

    # Charge transaction costs when position changes.
    data["Turnover"] = data["Position"].diff().abs().fillna(data["Position"].abs())

    data["TransactionCost"] = data["Turnover"] * TRANSACTION_COST

    data["StrategyReturn"] = data["StrategyReturnBeforeCost"] - data["TransactionCost"]

    print("Historical strategy simulation completed.")
    print("Transaction costs included.")

    return data


# --------------------------------------------------
# STEP 5: CALCULATE PERFORMANCE METRICS
# --------------------------------------------------


def calculate_performance(data):

    print("\nSTEP 5: CALCULATING PERFORMANCE")
    print("-" * 55)

    market_returns = data["MarketReturn"]

    strategy_returns = data["StrategyReturn"]

    # Compound returns
    market_total_return = (1 + market_returns).prod() - 1

    strategy_total_return = (1 + strategy_returns).prod() - 1

    # Annualized volatility
    volatility = strategy_returns.std() * np.sqrt(252)

    # Sharpe ratio using an illustrative 6% annual risk-free rate.
    risk_free_rate = 0.06

    daily_risk_free_rate = (1 + risk_free_rate) ** (1 / 252) - 1

    daily_std = strategy_returns.std()

    if daily_std > 0:

        sharpe_ratio = (
            np.sqrt(252) * (strategy_returns.mean() - daily_risk_free_rate) / daily_std
        )

    else:

        sharpe_ratio = 0.0

    # Maximum drawdown
    equity_curve = (1 + strategy_returns).cumprod()

    running_peak = equity_curve.cummax()

    drawdown = (equity_curve / running_peak) - 1

    max_drawdown = drawdown.min()

    return {
        "market_return": market_total_return,
        "strategy_return": strategy_total_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
    }


# --------------------------------------------------
# STEP 6: DISPLAY RESULTS
# --------------------------------------------------


def display_results(metrics, data):

    print("\nSTEP 6: BACKTEST RESULTS")
    print("=" * 60)

    print("Stock:", STOCK)

    print("Backtest observations:", len(data))

    print("\nBUY AND HOLD PERFORMANCE")

    print(f"Total return: " f"{metrics['market_return'] * 100:.2f}%")

    print("\nSMA STRATEGY PERFORMANCE")

    print(f"Total return: " f"{metrics['strategy_return'] * 100:.2f}%")

    print(f"Annualized volatility: " f"{metrics['volatility'] * 100:.2f}%")

    print(f"Sharpe ratio: " f"{metrics['sharpe_ratio']:.3f}")

    print(f"Maximum drawdown: " f"{metrics['max_drawdown'] * 100:.2f}%")

    print("\nSTRATEGY COMPARISON")

    if metrics["strategy_return"] > metrics["market_return"]:

        print("SMA strategy performed better in this period.")

    else:

        print("Buy-and-hold performed better in this period.")

    print("\nPASS: Backtesting completed.")

    print(
        "Note: Historical results do not guarantee future performance. "
        "Taxes, slippage and other costs are not fully modelled."
    )


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------


def main():

    print("=" * 60)

    print("CHRONOSMATCH - AI BACKTESTING ENGINE")

    print("MODULE 10")

    print("=" * 60)

    try:

        # Step 1
        data = collect_data()

        # Step 2
        data = calculate_indicators(data)

        # Step 3
        data = generate_positions(data)

        # Step 4
        data = calculate_strategy_returns(data)

        # Step 5
        metrics = calculate_performance(data)

        # Step 6
        display_results(metrics, data)

        return True

    except Exception as error:

        print("\nMODULE 10 ERROR:", error)

        return False


# --------------------------------------------------
# PROGRAM EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    success = main()

    if not success:
        raise SystemExit(1)
