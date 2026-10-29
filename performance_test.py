import asyncio
import time

from market_simulator import MarketSimulator
from ring_buffer import RingBuffer


async def consume_orders(ring_buffer, producer_task, results):
    """Consume orders while the producer is running."""

    consumed = 0
    checksum = 0

    while not producer_task.done() or not ring_buffer.is_empty():
        order = ring_buffer.read_order()

        if order is None:
            await asyncio.sleep(0)
            continue

        consumed += 1
        checksum += order["order_id"]

    results["consumed"] = consumed
    results["checksum"] = checksum


async def run_transfer_test(total_orders, label):
    """Measure order-transfer performance."""

    ring_buffer = RingBuffer()

    try:
        simulator = MarketSimulator(
            ring_buffer=ring_buffer,
            total_orders=total_orders,
        )

        consumer_results = {}

        print()
        print("=" * 55)
        print(label)
        print("=" * 55)

        start_time = time.perf_counter()

        producer_task = asyncio.create_task(
            simulator.generate_orders()
        )

        consumer_task = asyncio.create_task(
            consume_orders(
                ring_buffer,
                producer_task,
                consumer_results,
            )
        )

        producer_result, _ = await asyncio.gather(
            producer_task,
            consumer_task,
        )

        elapsed = time.perf_counter() - start_time

        consumed = consumer_results["consumed"]
        checksum = consumer_results["checksum"]

        expected_checksum = total_orders * (total_orders + 1) // 2

        passed = (
            producer_result["generated"] == total_orders
            and producer_result["failed"] == 0
            and producer_result["rejected"] == 0
            and consumed == total_orders
            and checksum == expected_checksum
            and ring_buffer.is_empty()
        )

        result = {
            "requested": total_orders,
            "generated": producer_result["generated"],
            "failed": producer_result["failed"],
            "rejected": producer_result["rejected"],
            "consumed": consumed,
            "checksum": checksum,
            "elapsed": elapsed,
            "throughput": consumed / elapsed if elapsed > 0 else 0,
            "passed": passed,
        }

        print(f"Orders requested: {result['requested']}")
        print(f"Orders generated: {result['generated']}")
        print(f"Orders failed: {result['failed']}")
        print(f"Orders rejected: {result['rejected']}")
        print(f"Orders consumed: {result['consumed']}")
        print(f"Order ID checksum: {result['checksum']}")
        print(f"Elapsed time: {result['elapsed']:.4f} seconds")
        print(
            f"Throughput: {result['throughput']:.2f} orders/second"
        )
        print(
            f"Validation: {'PASS' if result['passed'] else 'FAIL'}"
        )

        return result

    finally:
        ring_buffer.close()


if __name__ == "__main__":
    asyncio.run(run_transfer_test(500_000, "WEEK 3 PERFORMANCE TEST"))