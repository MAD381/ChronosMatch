from app.matching.order import create_order
from app.matching.matching_engine import MatchingEngine


def main():
    engine = MatchingEngine()

    orders = [
        create_order("B001", "ABC", "BUY", 100, 10),
        create_order("B002", "ABC", "BUY", 98, 5),
        create_order("S001", "ABC", "SELL", 100, 5),
        create_order("S002", "ABC", "SELL", 101, 5),
    ]

    for order in orders:
        engine.submit_order(order)

    print("\n========== EXECUTED TRADES ==========")

    for trade in engine.trades:
        print(trade)

    engine.order_book.display()


if __name__ == "__main__":
    main()