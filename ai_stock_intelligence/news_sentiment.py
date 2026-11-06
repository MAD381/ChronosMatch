"""
ChronosMatch - AI Stock Intelligence
Module 6: News and Sentiment Analysis
"""

import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def get_company_news(ticker):
    """Collect recent company news headlines."""

    try:
        print(f"\nFetching news for {ticker}...")

        stock = yf.Ticker(ticker)
        news = stock.news

        if not news:
            print("No news articles available.")
            return []

        headlines = []

        for article in news:
            content = article.get("content", {})

            if isinstance(content, dict):
                title = content.get("title", "")
                link = content.get("canonicalUrl", {})
                url = link.get("url", "") if isinstance(link, dict) else ""
            else:
                title = article.get("title", "")
                url = article.get("link", "")

            if title:
                headlines.append({"title": title, "url": url})

        return headlines

    except Exception as error:
        print(f"Error collecting news: {error}")
        return []


def analyze_sentiment(headline):
    """Classify a headline using VADER sentiment."""

    scores = analyzer.polarity_scores(headline)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "POSITIVE"
    elif compound <= -0.05:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return sentiment, compound


def display_news_report(ticker, headlines):
    """Display news and overall sentiment."""

    print("\nCHRONOSMATCH - NEWS SENTIMENT REPORT")
    print("=" * 50)

    if not headlines:
        print("No news headlines available for analysis.")
        return

    positive = 0
    negative = 0
    neutral = 0
    total_score = 0

    for index, article in enumerate(headlines, start=1):

        title = article["title"]

        sentiment, score = analyze_sentiment(title)

        total_score += score

        if sentiment == "POSITIVE":
            positive += 1
        elif sentiment == "NEGATIVE":
            negative += 1
        else:
            neutral += 1

        print(f"\nNews {index}: {title}")
        print(f"Sentiment: {sentiment}")
        print(f"Sentiment Score: {score:.3f}")

    average_score = total_score / len(headlines)

    if average_score >= 0.05:
        overall = "POSITIVE"
    elif average_score <= -0.05:
        overall = "NEGATIVE"
    else:
        overall = "NEUTRAL"

    print("\nOVERALL SENTIMENT SUMMARY")
    print("-" * 35)

    print(f"Stock: {ticker}")
    print(f"Total Headlines: {len(headlines)}")
    print(f"Positive News: {positive}")
    print(f"Negative News: {negative}")
    print(f"Neutral News: {neutral}")
    print(f"Average Sentiment Score: {average_score:.3f}")
    print(f"Overall News Sentiment: {overall}")

    print("\nNote: News sentiment is experimental.")
    print("It does not predict or guarantee stock movements.")


if __name__ == "__main__":

    ticker = "RELIANCE.NS"

    company_news = get_company_news(ticker)

    display_news_report(ticker, company_news)
