"""
CHRONOSMATCH - MODULE 12
AI Stock Intelligence: Interactive Stock Report

Creates an interactive HTML report containing:
1. Historical stock prices
2. 20-day Simple Moving Average
3. 50-day Simple Moving Average
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

TICKER = "RELIANCE.NS"
PERIOD = "1y"
OUTPUT_FILE = "chronosmatch_stock_report.html"


def collect_stock_data():
    """Download historical stock prices."""

    print(f"Downloading stock data for {TICKER}...")

    data = yf.download(
        TICKER, period=PERIOD, interval="1d", auto_adjust=True, progress=False
    )

    if data.empty:
        raise ValueError("No stock data received.")

    close = data["Close"]

    # Handle yfinance MultiIndex columns.
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    prices = close.dropna().to_frame(name="Close")

    if prices.empty:
        raise ValueError("No valid closing prices found.")

    return prices


def calculate_indicators(data):
    """Calculate moving averages."""

    data = data.copy()

    data["SMA_20"] = data["Close"].rolling(window=20).mean()

    data["SMA_50"] = data["Close"].rolling(window=50).mean()

    return data


def create_interactive_report(data):
    """Build and save the Plotly stock report."""

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=data.index, y=data["Close"], mode="lines", name="Stock Closing Price"
        )
    )

    figure.add_trace(
        go.Scatter(x=data.index, y=data["SMA_20"], mode="lines", name="20-Day SMA")
    )

    figure.add_trace(
        go.Scatter(x=data.index, y=data["SMA_50"], mode="lines", name="50-Day SMA")
    )

    figure.update_layout(
        title=f"{TICKER} - Interactive Stock Analysis",
        xaxis_title="Date",
        yaxis_title="Price (INR)",
        template="plotly_white",
        hovermode="x unified",
        legend_title="Indicators",
    )

    output_path = Path.cwd() / OUTPUT_FILE

    figure.write_html(str(output_path), include_plotlyjs=True, full_html=True)

    print("\nSTOCK REPORT CREATED SUCCESSFULLY")
    print("=" * 55)
    print(f"Stock              : {TICKER}")
    print(f"Records            : {len(data)}")
    print(f"Latest Close       : Rs. {data['Close'].iloc[-1]:.2f}")
    print(f"20-Day SMA         : Rs. {data['SMA_20'].iloc[-1]:.2f}")
    print(f"50-Day SMA         : Rs. {data['SMA_50'].iloc[-1]:.2f}")
    print(f"Report Location    : {output_path}")
    print("=" * 55)


def main():
    try:
        stock_data = collect_stock_data()
        stock_data = calculate_indicators(stock_data)
        create_interactive_report(stock_data)

    except Exception as error:
        print(f"Report generation failed: {error}")


if __name__ == "__main__":
    main()
