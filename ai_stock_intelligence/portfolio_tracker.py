"""
CHRONOSMATCH - MODULE 11
AI Stock Intelligence: Portfolio Tracker

Tracks sample stock holdings using historical market data.
This is an educational demo, not a live brokerage application.
"""

import yfinance as yf
import pandas as pd

# Sample portfolio holdings.
# Change the quantity and average buy price to test other values.
HOLDINGS = {
    "RELIANCE.NS": {"quantity": 2, "average_buy_price": 1200.00},
    "TCS.NS": {"quantity": 1, "average_buy_price": 3500.00},
    "INFY.NS": {"quantity": 3, "average_buy_price": 1500.00},
}


def get_latest_price(ticker):
    """Download recent data and return the latest closing price."""

    data = yf.download(
        ticker, period="5d", interval="1d", auto_adjust=True, progress=False
    )

    if data.empty:
        raise ValueError(f"No market data available for {ticker}")

    close_data = data["Close"]

    # Handle yfinance MultiIndex columns.
    if isinstance(close_data, pd.DataFrame):
        close_data = close_data.iloc[:, 0]

    close_data = close_data.dropna()

    if close_data.empty:
        raise ValueError(f"No valid closing price for {ticker}")

    return float(close_data.iloc[-1])


def calculate_holding(ticker, details):
    """Calculate investment value and unrealized profit or loss."""

    quantity = details["quantity"]
    buy_price = details["average_buy_price"]

    if quantity <= 0 or buy_price < 0:
        raise ValueError(f"Invalid holding details for {ticker}")

    current_price = get_latest_price(ticker)

    invested_amount = quantity * buy_price
    current_value = quantity * current_price

    profit_loss = current_value - invested_amount

    if invested_amount > 0:
        return_percentage = (profit_loss / invested_amount) * 100
    else:
        return_percentage = 0.0

    return {
        "quantity": quantity,
        "buy_price": buy_price,
        "current_price": current_price,
        "invested": invested_amount,
        "current_value": current_value,
        "profit_loss": profit_loss,
        "return_percentage": return_percentage,
    }


def run_portfolio_tracker():
    """Track all sample holdings and display portfolio summary."""

    print("\nCHRONOSMATCH - AI PORTFOLIO TRACKER")
    print("=" * 65)

    results = []

    for ticker, details in HOLDINGS.items():
        print(f"\nFetching data for {ticker}...")

        try:
            result = calculate_holding(ticker, details)
            results.append((ticker, result))

            print(f"Quantity          : {result['quantity']}")
            print(f"Average Buy Price : Rs. {result['buy_price']:.2f}")
            print(f"Current Price     : Rs. {result['current_price']:.2f}")
            print(f"Invested Amount   : Rs. {result['invested']:.2f}")
            print(f"Current Value     : Rs. {result['current_value']:.2f}")
            print(f"Profit/Loss       : Rs. {result['profit_loss']:.2f}")
            print(f"Return            : {result['return_percentage']:.2f}%")

        except Exception as error:
            print(f"Could not track {ticker}: {error}")

    print("\n" + "=" * 65)
    print("OVERALL PORTFOLIO SUMMARY")
    print("=" * 65)

    if not results:
        print("No holdings could be tracked.")
        return

    total_invested = sum(result["invested"] for _, result in results)

    total_value = sum(result["current_value"] for _, result in results)

    total_profit_loss = total_value - total_invested

    if total_invested > 0:
        total_return = (total_profit_loss / total_invested) * 100
    else:
        total_return = 0.0

    print(f"Stocks Tracked     : {len(results)}")
    print(f"Total Investment   : Rs. {total_invested:.2f}")
    print(f"Current Value      : Rs. {total_value:.2f}")
    print(f"Total Profit/Loss  : Rs. {total_profit_loss:.2f}")
    print(f"Portfolio Return   : {total_return:.2f}%")

    if total_profit_loss > 0:
        print("Portfolio Status  : PROFIT")
    elif total_profit_loss < 0:
        print("Portfolio Status  : LOSS")
    else:
        print("Portfolio Status  : BREAK EVEN")

    print("=" * 65)
    print("Portfolio tracking completed.")


if __name__ == "__main__":
    run_portfolio_tracker()
