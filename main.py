import asyncio
import time

from config import TOTAL_ORDERS
from market_simulator import MarketSimulator
from ring_buffer import RingBuffer


async def consume_orders(ring_buffer, total_orders, state):
    """
    Consume orders asynchronously.

    This function runs alongside the market simulator.
    """

    consumed = 0
    checksum = 0

    while consumed < total_orders:

        order = ring_buffer.read_order()

        if order is None:
            await asyncio.sleep(0)
            continue

        consumed += 1
        checksum += order["order_id"]

    state["consumed"] = consumed
    state["checksum"] = checksum


async def main():
    print("=" * 55)
    print("       CHRONOSMATCH - WEEK 1 PROTOTYPE")
    print("=" * 55)

    ring_buffer = RingBuffer()

    simulator = MarketSimulator(
        ring_buffer=ring_buffer,
        total_orders=TOTAL_ORDERS,
    )

    consumer_state = {}

    start_time = time.perf_counter()

    try:
        producer_task = asyncio.create_task(
            simulator.generate_orders()
        )

        consumer_task = asyncio.create_task(
            consume_orders(
                ring_buffer,
                TOTAL_ORDERS,
                consumer_state,
            )
        )

        producer_result, _ = await asyncio.gather(
            producer_task,
            consumer_task,
        )

        total_elapsed = time.perf_counter() - start_time

        print("\nWEEK 1 RESULTS")
        print("-" * 55)

        print(
            f"Orders successfully generated: "
            f"{producer_result['generated']}"
        )

        print(
            f"Orders rejected: "
            f"{producer_result['failed']}"
        )

        print(
            f"Orders consumed: "
            f"{consumer_state['consumed']}"
        )

        print(
            f"Order ID checksum: "
            f"{consumer_state['checksum']}"
        )

        print(
            f"Producer elapsed time: "
            f"{producer_result['elapsed_seconds']:.4f} seconds"
        )

        print(
            f"Total elapsed time: "
            f"{total_elapsed:.4f} seconds"
        )

        if total_elapsed > 0:
            print(
                f"End-to-end throughput: "
                f"{consumer_state['consumed'] / total_elapsed:.2f} "
                f"orders/second"
            )

        expected_checksum = (
            TOTAL_ORDERS * (TOTAL_ORDERS + 1) // 2
        )

        print("\nVALIDATION")
        print("-" * 55)

        if (
            producer_result["generated"] == TOTAL_ORDERS
            and producer_result["failed"] == 0
            and consumer_state["consumed"] == TOTAL_ORDERS
            and consumer_state["checksum"] == expected_checksum
        ):
            print("PASS: All orders were transferred and verified.")
        else:
            print("FAIL: Order validation did not pass.")

    finally:
        ring_buffer.close()

    print("\nWeek 1 prototype finished.")


if __name__ == "__main__":
    asyncio.run(main())