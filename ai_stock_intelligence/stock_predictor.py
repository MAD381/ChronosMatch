"""
ChronosMatch - AI Stock Intelligence
Module 3: Machine Learning Stock Predictor

Uses Random Forest to estimate the next trading
session's price direction and closing price.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from ai_stock_intelligence.data_collector import get_stock_history
from ai_stock_intelligence.technical_analysis import calculate_indicators

FEATURES = [
    "SMA_20",
    "SMA_50",
    "EMA_20",
    "RSI",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "BB_Upper",
    "BB_Lower",
    "Volume",
]


def prepare_training_data(data):
    """Prepare historical features and next-day targets."""

    data = data.copy()

    # Target: next trading session's closing price.
    data["Next_Close"] = data["Close"].shift(-1)

    # Target: 1 if next close is higher, otherwise 0.
    data["Direction"] = (data["Next_Close"] > data["Close"]).astype(int)

    data.dropna(inplace=True)

    return data


def train_models(data):
    """Train direction and closing-price models."""

    data = prepare_training_data(data)

    X = data[FEATURES]
    y_direction = data["Direction"]
    y_price = data["Next_Close"]

    if len(data) < 100:
        raise ValueError("Not enough historical data to train the models.")

    # Use chronological splitting to avoid future-data leakage.
    split = int(len(data) * 0.8)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_direction_train = y_direction.iloc[:split]
    y_direction_test = y_direction.iloc[split:]

    y_price_train = y_price.iloc[:split]
    y_price_test = y_price.iloc[split:]

    # Direction classification model.
    direction_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=3,
        random_state=42,
        class_weight="balanced",
    )

    direction_model.fit(X_train, y_direction_train)

    direction_predictions = direction_model.predict(X_test)

    accuracy = accuracy_score(y_direction_test, direction_predictions)

    # Next closing-price regression model.
    price_model = RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=3, random_state=42
    )

    price_model.fit(X_train, y_price_train)

    price_predictions = price_model.predict(X_test)

    mae = mean_absolute_error(y_price_test, price_predictions)

    return direction_model, price_model, accuracy, mae, data


def predict_next_session(direction_model, price_model, data):
    """Estimate the next session's direction and closing price."""

    latest_features = data[FEATURES].iloc[[-1]]

    direction = direction_model.predict(latest_features)[0]

    probabilities = direction_model.predict_proba(latest_features)[0]

    class_positions = list(direction_model.classes_)
    up_probability = probabilities[class_positions.index(1)]

    predicted_price = price_model.predict(latest_features)[0]

    current_price = data["Close"].iloc[-1]

    movement = "UP" if direction == 1 else "DOWN OR UNCHANGED"

    return movement, up_probability, predicted_price, current_price


if __name__ == "__main__":

    ticker = "RELIANCE.NS"

    print("\nCHRONOSMATCH - AI STOCK PREDICTOR")
    print("=" * 45)

    # Collect historical data.
    stock_data = get_stock_history(ticker)

    if stock_data is not None:

        # Calculate technical indicators.
        analysed_data = calculate_indicators(stock_data)

        # Train the machine-learning models.
        direction_model, price_model, accuracy, mae, training_data = train_models(
            analysed_data
        )

        # Estimate the next trading session.
        movement, probability, predicted_price, current_price = predict_next_session(
            direction_model, price_model, analysed_data
        )

        print("\nMODEL EVALUATION")
        print("-" * 30)
        print(f"Historical direction accuracy: {accuracy * 100:.2f}%")
        print(f"Historical price MAE: Rs. {mae:.2f}")

        print("\nNEXT SESSION ESTIMATE")
        print("-" * 30)
        print(f"Stock: {ticker}")
        print(f"Latest closing price: Rs. {current_price:.2f}")
        print(f"Estimated direction: {movement}")
        print(f"Estimated closing price: Rs. {predicted_price:.2f}")
        print(f"Model probability of upward movement: {probability * 100:.2f}%")

        print("\nNote: Experimental model output, not financial advice.")
        print("Predictions are uncertain and do not guarantee returns.")
