class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side == "BUY":
            self.buy_orders.append(order)

        elif order.side == "SELL":
            self.sell_orders.append(order)

    def get_best_bid(self):
        if not self.buy_orders:
            return None

        return max(
            self.buy_orders,
            key=lambda order: (order.price, -order.timestamp)
        )

    def get_best_ask(self):
        if not self.sell_orders:
            return None

        return min(
            self.sell_orders,
            key=lambda order: (order.price, order.timestamp)
        )

    def display(self):
        print("\n========== ORDER BOOK ==========")

        print("\nBUY ORDERS:")
        for order in sorted(
            self.buy_orders,
            key=lambda order: (-order.price, order.timestamp)
        ):
            print(
                f"{order.order_id} | "
                f"Price: {order.price} | "
                f"Quantity: {order.quantity}"
            )

        print("\nSELL ORDERS:")
        for order in sorted(
            self.sell_orders,
            key=lambda order: (order.price, order.timestamp)
        ):
            print(
                f"{order.order_id} | "
                f"Price: {order.price} | "
                f"Quantity: {order.quantity}"
            )

        print("================================")