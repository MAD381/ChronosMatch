from dataclasses import dataclass
from time import time


@dataclass
class Order:
    order_id: str
    symbol: str
    side: str
    price: float
    quantity: int
    timestamp: float

    def __post_init__(self):
        self.side = self.side.upper()

        if self.side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")

        if self.price <= 0:
            raise ValueError("Price must be greater than zero")

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")


def create_order(order_id, symbol, side, price, quantity):
    return Order(
        order_id=order_id,
        symbol=symbol,
        side=side,
        price=price,
        quantity=quantity,
        timestamp=time()
    )