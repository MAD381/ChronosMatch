"""
CHRONOSMATCH - MODULE 9
AI TRADING SIGNAL GENERATOR

Features:
1. Collect historical stock data.
2. Calculate SMA 20 and SMA 50.
3. Calculate EMA 20.
4. Calculate RSI.
5. Generate BUY, HOLD or SELL signals.
6. Display the analysis results.

Educational project only. No actual trades are placed.
"""

import pandas as pd
import yfinance as yf

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

STOCK = "RELIANCE.NS"
PERIOD = "1y"


# --------------------------------------------------
# STEP 1: COLLECT STOCK DATA
# --------------------------------------------------


def collect_data():

    print("\nSTEP 1: COLLECTING STOCK DATA")
    print("-" * 50)

    data = yf.download(
        STOCK, period=PERIOD, interval="1d", auto_adjust=True, progress=False
    )

    if data.empty:
        raise RuntimeError("Stock data is unavailable.")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if "Close" not in data.columns:
        raise RuntimeError("Closing price data is missing.")

    data = data.dropna(subset=["Close"]).copy()

    print("Stock data downloaded successfully.")
    print("Total records:", len(data))

    return data


# --------------------------------------------------
# STEP 2: CALCULATE TECHNICAL INDICATORS
# --------------------------------------------------


def calculate_indicators(data):

    print("\nSTEP 2: CALCULATING INDICATORS")
    print("-" * 50)

    close = data["Close"].astype(float)

    data["SMA20"] = close.rolling(window=20).mean()

    data["SMA50"] = close.rolling(window=50).mean()

    data["EMA20"] = close.ewm(span=20, adjust=False).mean()

    # RSI calculation
    difference = close.diff()

    gains = difference.clip(lower=0)

    losses = -difference.clip(upper=0)

    average_gain = gains.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()

    average_loss = losses.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()

    relative_strength = average_gain / average_loss.replace(0, float("nan"))

    data["RSI"] = 100 - (100 / (1 + relative_strength))

    # Handle cases where prices only rise or never change.
    data.loc[(average_loss == 0) & (average_gain > 0), "RSI"] = 100

    data.loc[(average_loss == 0) & (average_gain == 0), "RSI"] = 50

    print("SMA 20 calculated.")
    print("SMA 50 calculated.")
    print("EMA 20 calculated.")
    print("RSI 14 calculated.")

    return data


# --------------------------------------------------
# STEP 3: GENERATE TRADING SIGNAL
# --------------------------------------------------


def generate_signal(data):

    print("\nSTEP 3: GENERATING TRADING SIGNAL")
    print("-" * 50)

    latest = data.iloc[-1]

    price = float(latest["Close"])

    sma20 = float(latest["SMA20"])

    sma50 = float(latest["SMA50"])

    ema20 = float(latest["EMA20"])

    rsi = float(latest["RSI"])

    score = 0

    # Price and moving-average trend
    if price > sma20:
        score += 1
    else:
        score -= 1

    if sma20 > sma50:
        score += 1
    else:
        score -= 1

    if price > ema20:
        score += 1
    else:
        score -= 1

    # RSI interpretation
    if rsi < 30:
        score += 1
    elif rsi > 70:
        score -= 1

    if score >= 2:
        signal = "BUY"

    elif score <= -2:
        signal = "SELL"

    else:
        signal = "HOLD"

    return {
        "price": price,
        "sma20": sma20,
        "sma50": sma50,
        "ema20": ema20,
        "rsi": rsi,
        "score": score,
        "signal": signal,
    }


# --------------------------------------------------
# STEP 4: DISPLAY RESULTS
# --------------------------------------------------


def display_results(result):

    print("\nSTEP 4: TRADING ANALYSIS")
    print("=" * 55)

    print("Stock:", STOCK)

    print(f"Latest adjusted close: Rs. {result['price']:.2f}")

    print(f"SMA 20: Rs. {result['sma20']:.2f}")

    print(f"SMA 50: Rs. {result['sma50']:.2f}")

    print(f"EMA 20: Rs. {result['ema20']:.2f}")

    print(f"RSI 14: {result['rsi']:.2f}")

    print("\nSignal score:", result["score"])

    print("\nFINAL TRADING SIGNAL")
    print("-" * 55)

    print("SIGNAL:", result["signal"])

    if result["signal"] == "BUY":
        print("Technical indicators show a positive trend.")

    elif result["signal"] == "SELL":
        print("Technical indicators show a negative trend.")

    else:
        print("Technical indicators show a mixed or neutral trend.")

    print("\nPASS: Trading signal generated.")

    print(
        "Note: This is a rule-based educational signal, "
        "not a financial recommendation."
    )


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------


def main():

    print("=" * 55)

    print("CHRONOSMATCH - AI TRADING SIGNAL GENERATOR")

    print("MODULE 9")

    print("=" * 55)

    try:

        data = collect_data()

        data = calculate_indicators(data)

        result = generate_signal(data)

        display_results(result)

        return True

    except Exception as error:

        print("\nMODULE 9 ERROR:", error)

        return False


# --------------------------------------------------
# PROGRAM EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    success = main()

    if not success:
        raise SystemExit(1)
