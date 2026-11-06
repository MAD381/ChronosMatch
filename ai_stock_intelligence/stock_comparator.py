"""
ChronosMatch - AI Stock Intelligence
Module 7: Stock Comparison Analyzer

Compares multiple companies using historical returns,
volatility, RSI and selected financial ratios.
"""

import yfinance as yf
import pandas as pd
import numpy as np

from ai_stock_intelligence.data_collector import get_stock_history
from ai_stock_intelligence.technical_analysis import calculate_indicators


def compare_stock(ticker):
    """Collect comparison metrics for one stock."""

    print(f"\nAnalyzing {ticker}...")

    try:
        data = get_stock_history(ticker, period="1y")

        if data is None or len(data) < 50:
            print(f"Insufficient historical data for {ticker}.")
            return None

        # Calculate technical indicators.
        analysis = calculate_indicators(data)
        latest = analysis.iloc[-1]

        # Calculate historical return.
        first_price = data["Close"].iloc[0]
        last_price = data["Close"].iloc[-1]

        total_return = ((last_price / first_price) - 1) * 100

        # Calculate annualized historical volatility.
        daily_returns = data["Close"].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252) * 100

        # Collect company financial information.
        info = yf.Ticker(ticker).info

        return {
            "ticker": ticker,
            "price": float(last_price),
            "return": float(total_return),
            "volatility": float(volatility),
            "rsi": float(latest["RSI"]),
            "pe_ratio": info.get("trailingPE"),
            "roe": info.get("returnOnEquity"),
        }

    except Exception as error:
        print(f"Could not analyze {ticker}: {error}")
        return None


def display_comparison(results):
    """Display a comparison table."""

    print("\nCHRONOSMATCH - STOCK COMPARISON REPORT")
    print("=" * 75)

    if not results:
        print("No stocks could be compared.")
        return

    table = pd.DataFrame(results)

    table.rename(
        columns={
            "ticker": "Stock",
            "price": "Latest Price (Rs.)",
            "return": "1Y Return (%)",
            "volatility": "Volatility (%)",
            "rsi": "RSI",
            "pe_ratio": "P/E Ratio",
            "roe": "ROE",
        },
        inplace=True,
    )

    print(
        table.to_string(
            index=False,
            formatters={
                "Latest Price (Rs.)": lambda x: f"{x:.2f}",
                "1Y Return (%)": lambda x: f"{x:.2f}",
                "Volatility (%)": lambda x: f"{x:.2f}",
                "RSI": lambda x: f"{x:.2f}",
                "P/E Ratio": lambda x: (f"{x:.2f}" if pd.notna(x) else "N/A"),
                "ROE": lambda x: (f"{x * 100:.2f}%" if pd.notna(x) else "N/A"),
            },
        )
    )

    # Rank stocks by historical one-year return.
    ranked = sorted(results, key=lambda item: item["return"], reverse=True)

    print("\nHISTORICAL RETURN RANKING")
    print("-" * 35)

    for position, stock in enumerate(ranked, start=1):
        print(f"{position}. {stock['ticker']} " f"- {stock['return']:.2f}%")

    print("\nNote:")
    print("Past returns do not predict future performance.")
    print("This comparison is not investment advice.")


if __name__ == "__main__":

    # Example NSE-listed companies.
    tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]

    comparison_results = []

    for ticker in tickers:
        result = compare_stock(ticker)

        if result is not None:
            comparison_results.append(result)

    display_comparison(comparison_results)
