import time

class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book
        self.trade_counter = 1
        self.trade_history = []

    def process_order(self, order):
        print(f"[{order.side}] Processing Order ID: {order.order_id} | Price: {order.price} | Qty: {order.quantity}")
        executed_trades = []

        # Continuous matching loop (Price-Time Priority)
        while self.order_book.get_best_bid() and self.order_book.get_best_ask():
            best_bid = self.order_book.get_best_bid()
            best_ask = self.order_book.get_best_ask()

            # Match condition: Highest Buy price >= Lowest Sell price
            if best_bid.price >= best_ask.price:
                trade_qty = min(best_bid.quantity, best_ask.quantity)
                trade_price = best_ask.price  # Match at the resting order price

                trade_info = {
                    "trade_id": self.trade_counter,
                    "buyer_id": best_bid.order_id,
                    "seller_id": best_ask.order_id,
                    "quantity": trade_qty,
                    "price": trade_price,
                    "timestamp": time.time()
                }
                
                self.trade_history.append(trade_info)
                executed_trades.append(trade_info)
                print(f"   --> MATCH! Buyer {best_bid.order_id} & Seller {best_ask.order_id}: {trade_qty} units @ ${trade_price}")
                
                self.trade_counter += 1

                # Update quantities
                best_bid.quantity -= trade_qty
                best_ask.quantity -= trade_qty

                # Remove fully filled orders from the lists
                if best_bid.quantity == 0:
                    self.order_book.buy_orders.remove(best_bid)
                if best_ask.quantity == 0:
                    self.order_book.sell_orders.remove(best_ask)
            else:
                break

        # If order is not fully filled, add remainder to the order book
        if order.quantity > 0:
            self.order_book.add_order(order)

        return executed_trades