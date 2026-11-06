"""
ChronosMatch - AI Stock Intelligence
Module 2: Technical Analysis
"""

import pandas as pd
from ai_stock_intelligence.data_collector import get_stock_history


def calculate_indicators(data):
    """Calculate technical indicators from historical stock data."""

    if data is None or data.empty:
        raise ValueError("No stock data available for analysis.")

    data = data.copy()

    # 1. Simple Moving Averages
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()

    # 2. Exponential Moving Average
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()

    # 3. Relative Strength Index (RSI)
    price_change = data["Close"].diff()

    gains = price_change.clip(lower=0)
    losses = -price_change.clip(upper=0)

    average_gain = gains.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()

    average_loss = losses.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()

    relative_strength = average_gain / average_loss

    data["RSI"] = 100 - (100 / (1 + relative_strength))

    # Handle periods with no losses.
    data.loc[(average_loss == 0) & (average_gain > 0), "RSI"] = 100

    data.loc[(average_loss == 0) & (average_gain == 0), "RSI"] = 50

    # 4. MACD
    ema_12 = data["Close"].ewm(span=12, adjust=False).mean()

    ema_26 = data["Close"].ewm(span=26, adjust=False).mean()

    data["MACD"] = ema_12 - ema_26

    data["MACD_Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()

    data["MACD_Histogram"] = data["MACD"] - data["MACD_Signal"]

    # 5. Bollinger Bands
    middle_band = data["Close"].rolling(window=20).mean()

    standard_deviation = data["Close"].rolling(window=20).std()

    data["BB_Upper"] = middle_band + (2 * standard_deviation)
    data["BB_Lower"] = middle_band - (2 * standard_deviation)

    return data


if __name__ == "__main__":

    ticker = "RELIANCE.NS"

    # Collect historical data.
    stock_data = get_stock_history(ticker)

    if stock_data is not None:

        # Calculate technical indicators.
        analysis = calculate_indicators(stock_data)

        print("\nCHRONOSMATCH - TECHNICAL ANALYSIS")
        print("=" * 45)

        print("\nLatest stock analysis:")
        print(analysis.tail(5).round(2).to_string())

        latest = analysis.iloc[-1]

        print("\nLATEST INDICATOR VALUES")
        print("-" * 30)

        print(f"Closing Price: {latest['Close']:.2f}")
        print(f"SMA 20: {latest['SMA_20']:.2f}")
        print(f"SMA 50: {latest['SMA_50']:.2f}")
        print(f"EMA 20: {latest['EMA_20']:.2f}")
        print(f"RSI: {latest['RSI']:.2f}")
        print(f"MACD: {latest['MACD']:.2f}")
        print(f"MACD Signal: {latest['MACD_Signal']:.2f}")
        print(f"Bollinger Upper: {latest['BB_Upper']:.2f}")
        print(f"Bollinger Lower: {latest['BB_Lower']:.2f}")
