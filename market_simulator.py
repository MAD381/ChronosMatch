
import asyncio
import random
import struct 
import time


class MarketSimulator:
    """Generate mock trading orders for ChronosMatch."""

    def __init__(self, ring_buffer, total_orders=100_000):
        self.ring_buffer = ring_buffer
        self.total_orders = total_orders

        self.generated_orders = 0
        self.failed_orders = 0
        self.rejected_orders = 0

    async def generate_orders(self):
        """Generate orders and retry briefly when the buffer is full."""

        start_time = time.perf_counter()

        for order_id in range(1, self.total_orders + 1):
            price_paise = random.randint(100_000, 1_000_000)
            quantity = random.randint(1, 1000)

            written = False
            rejected = False

            for _ in range(100):
                try:
                    written = self.ring_buffer.write_order(
                        order_id,
                        price_paise,
                        quantity,
                    )
                except ValueError:
                    self.rejected_orders += 1
                    rejected = True
                    break

                if written:
                    self.generated_orders += 1
                    break

                # Give a concurrently running consumer time to read.
                await asyncio.sleep(0.001)

            if not written and not rejected:
                self.failed_orders += 1

            if order_id % 100 == 0:
                await asyncio.sleep(0)

        elapsed = time.perf_counter() - start_time

        return {
            "generated": self.generated_orders,
            "failed": self.failed_orders,
            "rejected": self.rejected_orders,
            "elapsed_seconds": elapsed,
        }
