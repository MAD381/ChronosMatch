"""
ChronosMatch - AI Stock Intelligence
Module 4: Stock Risk Analyzer

Calculates returns, volatility, maximum drawdown
and a basic historical risk classification.
"""

import numpy as np
import pandas as pd

from ai_stock_intelligence.data_collector import get_stock_history


def calculate_risk(data):
    """Calculate historical risk measurements."""

    if data is None or data.empty:
        raise ValueError("No stock data available.")

    data = data.copy()

    if "Close" not in data.columns:
        raise ValueError("Closing price column is missing.")

    # Calculate daily percentage returns.
    data["Daily_Return"] = data["Close"].pct_change()

    returns = data["Daily_Return"].dropna()

    if len(returns) < 2:
        raise ValueError("Not enough data to calculate risk.")

    # 1. Annualized volatility.
    daily_volatility = returns.std()
    annual_volatility = daily_volatility * np.sqrt(252) * 100

    # 2. Average daily return.
    average_daily_return = returns.mean() * 100

    # 3. Maximum drawdown.
    running_peak = data["Close"].cummax()
    drawdown = (data["Close"] / running_peak) - 1

    maximum_drawdown = drawdown.min() * 100

    # 4. Annualized historical return.
    total_return = (data["Close"].iloc[-1] / data["Close"].iloc[0]) ** (
        252 / len(returns)
    ) - 1

    annual_return = total_return * 100

    # 5. Historical risk classification.
    if annual_volatility < 15:
        risk_level = "LOW"
    elif annual_volatility < 30:
        risk_level = "MODERATE"
    else:
        risk_level = "HIGH"

    return {
        "daily_volatility": daily_volatility * 100,
        "annual_volatility": annual_volatility,
        "average_daily_return": average_daily_return,
        "annual_return": annual_return,
        "maximum_drawdown": maximum_drawdown,
        "risk_level": risk_level,
    }


def display_risk_report(ticker, results):
    """Display the stock risk report."""

    print("\nCHRONOSMATCH - STOCK RISK REPORT")
    print("=" * 45)

    print(f"Stock: {ticker}")

    print("\nRISK MEASUREMENTS")
    print("-" * 30)

    print(f"Daily Volatility: " f"{results['daily_volatility']:.2f}%")

    print(f"Annualized Volatility: " f"{results['annual_volatility']:.2f}%")

    print(f"Average Daily Return: " f"{results['average_daily_return']:.2f}%")

    print(f"Annualized Historical Return: " f"{results['annual_return']:.2f}%")

    print(f"Maximum Drawdown: " f"{results['maximum_drawdown']:.2f}%")

    print("\nRISK CLASSIFICATION")
    print("-" * 30)

    print(f"Risk Level: {results['risk_level']}")

    print("\nNote: Historical risk measurements do not")
    print("guarantee future performance.")


if __name__ == "__main__":

    ticker = "RELIANCE.NS"

    # Download historical stock data.
    stock_data = get_stock_history(ticker)

    if stock_data is not None:

        # Calculate risk measurements.
        risk_results = calculate_risk(stock_data)

        # Display the report.
        display_risk_report(ticker, risk_results)
