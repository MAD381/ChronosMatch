import asyncio
import time

from market_simulator import MarketSimulator
from ring_buffer import RingBuffer


async def consume_orders(ring_buffer, producer_task, results):
    """Consume orders while the producer is running."""

    consumed = 0
    checksum = 0

    # Keep polling the ring buffer until the producer finishes and the buffer is completely empty
    while not producer_task.done() or not ring_buffer.is_empty():
        order = ring_buffer.read_order()

        # If buffer is temporarily empty, yield control back to the event loop to let the producer run
        if order is None:
            await asyncio.sleep(0)
            continue

        consumed += 1
        checksum += order["order_id"]  # Accumulate order IDs for integrity verification

    # Store final metrics in the results dictionary for validation
    results["consumed"] = consumed
    results["checksum"] = checksum


async def run_transfer_test(total_orders, label):
    """Measure order-transfer performance."""

    # Initialize the high-performance memory-mapped ring buffer
    ring_buffer = RingBuffer()

    try:
        # Bind the market simulator to the ring buffer for order injection
        simulator = MarketSimulator(
            ring_buffer=ring_buffer,
            total_orders=total_orders,
        )

        consumer_results = {}

        print()
        print("=" * 55)
        print(label)
        print("=" * 55)

        # Start high-precision performance timer
        start_time = time.perf_counter()

        # Concurrently run the order producer and consumer tasks
        producer_task = asyncio.create_task(simulator.generate_orders())

        consumer_task = asyncio.create_task(
            consume_orders(
                ring_buffer,
                producer_task,
                consumer_results,
            )
        )

        # Wait for both asynchronous tasks to complete execution
        producer_result, _ = await asyncio.gather(
            producer_task,
            consumer_task,
        )

        # Calculate total elapsed time
        elapsed = time.perf_counter() - start_time

        consumed = consumer_results["consumed"]
        checksum = consumer_results["checksum"]

        # Mathematical expected checksum for sequential order IDs (1 to N)
        expected_checksum = total_orders * (total_orders + 1) // 2

        # Validate that all orders were successfully generated, consumed, and matched checksums
        passed = (
            producer_result["generated"] == total_orders
            and producer_result["failed"] == 0
            and producer_result["rejected"] == 0
            and consumed == total_orders
            and checksum == expected_checksum
            and ring_buffer.is_empty()
        )

        # Compile performance metrics dictionary
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

        # Print structured metrics report
        print(f"Orders requested: {result['requested']}")
        print(f"Orders generated: {result['generated']}")
        print(f"Orders failed: {result['failed']}")
        print(f"Orders rejected: {result['rejected']}")
        print(f"Orders consumed: {result['consumed']}")
        print(f"Order ID checksum: {result['checksum']}")
        print(f"Elapsed time: {result['elapsed']:.4f} seconds")
        print(f"Throughput: {result['throughput']:.2f} orders/second")
        print(f"Validation: {'PASS' if result['passed'] else 'FAIL'}")

        return result

    finally:
        # Ensure memory-mapped buffers and file handles are safely closed
        ring_buffer.close()


if __name__ == "__main__":
    # Execute the 500,000-order throughput validation benchmark
    asyncio.run(run_transfer_test(500_000, "WEEK 3 PERFORMANCE TEST"))
