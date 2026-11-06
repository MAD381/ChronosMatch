"""
ChronosMatch - AI Stock Intelligence
Module 1: Historical Stock Data Collection
"""

import yfinance as yf
import pandas as pd


def get_stock_history(ticker, period="1y", interval="1d"):
    """
    Download historical stock market data.
    Example: RELIANCE.NS for Reliance Industries.
    """

    try:
        print(f"\nFetching stock data for {ticker}...")

        data = yf.download(
            ticker, period=period, interval=interval, auto_adjust=True, progress=False
        )

        if data.empty:
            print("No stock data found. Check the ticker symbol.")
            return None

        # Handle multiple-level column names.
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        required_columns = ["Open", "High", "Low", "Close", "Volume"]

        missing = [col for col in required_columns if col not in data.columns]

        if missing:
            print(f"Missing columns: {missing}")
            return None

        data = data[required_columns].copy()
        data.dropna(inplace=True)

        if data.empty:
            print("No valid records available.")
            return None

        print(f"Successfully collected {len(data)} records!")

        return data

    except Exception as error:
        print(f"Error collecting stock data: {error}")
        return None


if __name__ == "__main__":

    # Test with Reliance Industries (NSE).
    stock_data = get_stock_history("RELIANCE.NS")

    if stock_data is not None:
        print("\nLatest stock records:")
        print(stock_data.tail())

        print("\nStock data summary:")
        print(stock_data.describe())
