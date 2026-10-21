import asyncio
import random
import time
from dataclasses import dataclass


@dataclass
class Order:
    order_id: int
    timestamp_ns: int
    side: str
    price: float
    quantity: int
    symbol: str


class OrderSimulator:
    def __init__(
        self,
        total_orders: int = 100,
        interval: float = 0.001,
    ):
        self.total_orders = total_orders
        self.interval = interval
        self.order_id = 0

        self.symbols = ["AAPL", "GOOG", "MSFT", "NVDA"]

    async def generate_orders(self):
        """Generate mock trading orders asynchronously."""

        for _ in range(self.total_orders):
            self.order_id += 1

            order = Order(
                order_id=self.order_id,
                timestamp_ns=time.time_ns(),
                side=random.choice(["BUY", "SELL"]),
                price=round(random.uniform(99.0, 101.0), 2),
                quantity=random.randint(1, 100),
                symbol=random.choice(self.symbols),
            )

            yield order

            await asyncio.sleep(self.interval)


async def main():
    simulator = OrderSimulator(
        total_orders=10,
        interval=0.001,
    )

    generated_count = 0

    async for order in simulator.generate_orders():
        print(order)
        generated_count += 1

    print("\nSimulation completed.")
    print(f"Total orders generated: {generated_count}")


if __name__ == "__main__":
    asyncio.run(main())