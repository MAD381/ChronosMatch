"""
ChronosMatch - AI Stock Intelligence
Module 5: Company Fundamentals Analyzer

Analyzes company financial information using Yahoo Finance.
"""

import yfinance as yf


def get_fundamentals(ticker):
    """Collect important company financial information."""

    try:
        print(f"\nFetching company information for {ticker}...")

        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or not info.get("longName"):
            print("Company information is unavailable.")
            return None

        fundamentals = {
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap"),
            "revenue": info.get("totalRevenue"),
            "profit": info.get("netIncomeToCommon"),
            "eps": info.get("trailingEps"),
            "pe_ratio": info.get("trailingPE"),
            "debt_to_equity": info.get("debtToEquity"),
            "roe": info.get("returnOnEquity"),
            "profit_margin": info.get("profitMargins"),
            "current_price": info.get("currentPrice"),
        }

        return fundamentals

    except Exception as error:
        print(f"Error collecting company information: {error}")
        return None


def format_value(value, percentage=False):
    """Format financial values for display."""

    if value is None:
        return "Not available"

    if percentage:
        return f"{value * 100:.2f}%"

    return f"{value:,.2f}"


def analyze_financial_health(data):
    """Create a basic financial health summary."""

    if data is None:
        return "Insufficient data"

    positive = 0
    negative = 0

    # Check profitability.
    profit = data["profit"]
    if profit is not None:
        if profit > 0:
            positive += 1
        else:
            negative += 1

    # Check return on equity.
    roe = data["roe"]
    if roe is not None:
        if roe > 0:
            positive += 1
        else:
            negative += 1

    # Check profit margin.
    margin = data["profit_margin"]
    if margin is not None:
        if margin > 0:
            positive += 1
        else:
            negative += 1

    # A simple summary based on available indicators.
    if positive + negative == 0:
        return "Insufficient data"

    if positive > negative:
        return "More positive indicators"
    elif negative > positive:
        return "More negative indicators"
    else:
        return "Mixed financial indicators"


def display_report(data):
    """Display the company fundamentals report."""

    print("\nCHRONOSMATCH - COMPANY FUNDAMENTALS")
    print("=" * 50)

    print(f"Company: {data['company_name']}")
    print(f"Sector: {data['sector']}")
    print(f"Industry: {data['industry']}")

    print("\nFINANCIAL INFORMATION")
    print("-" * 35)

    print(f"Market Capitalization: {format_value(data['market_cap'])}")
    print(f"Revenue: {format_value(data['revenue'])}")
    print(f"Net Profit: {format_value(data['profit'])}")
    print(f"Earnings Per Share: {format_value(data['eps'])}")
    print(f"P/E Ratio: {format_value(data['pe_ratio'])}")
    print(f"Debt-to-Equity: {format_value(data['debt_to_equity'])}")
    print(f"Return on Equity: {format_value(data['roe'], True)}")
    print(f"Profit Margin: {format_value(data['profit_margin'], True)}")
    print(f"Reported Current Price: {format_value(data['current_price'])}")

    print("\nFINANCIAL HEALTH SUMMARY")
    print("-" * 35)

    health = analyze_financial_health(data)
    print(f"Summary: {health}")

    print("\nNote:")
    print("This is a basic screening tool, not a complete")
    print("financial assessment or investment recommendation.")


if __name__ == "__main__":

    ticker = "RELIANCE.NS"

    fundamentals = get_fundamentals(ticker)

    if fundamentals is not None:
        display_report(fundamentals)
