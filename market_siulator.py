import asyncio
import random
import time


class MarketSimulator:
    """
    Asynchronous mock trading order generator.
    """

    def __init__(self, ring_buffer, total_orders=100_000):
        self.ring_buffer = ring_buffer
        self.total_orders = total_orders

        self.generated_orders = 0
        self.failed_orders = 0

    async def generate_orders(self):
        """
        Generate mock orders and write them to the ring buffer.

        The consumer is allowed to run between batches.
        """

        start_time = time.perf_counter()

        for order_id in range(1, self.total_orders + 1):

            price_paise = random.randint(100_000, 1_000_000)
            quantity = random.randint(1, 1000)

            written = self.ring_buffer.write_order(
                order_id,
                price_paise,
                quantity,
            )

            if written:
                self.generated_orders += 1
            else:
                self.failed_orders += 1

            # Give the consumer an opportunity to run.
            if order_id % 100 == 0:
                await asyncio.sleep(0)

        elapsed = time.perf_counter() - start_time

        return {
            "generated": self.generated_orders,
            "failed": self.failed_orders,
            "elapsed_seconds": elapsed,
        }