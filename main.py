
import asyncio
import time

from config import TOTAL_ORDERS
from market_simulator import MarketSimulator
from ring_buffer import RingBuffer


def run_ipc_checks(ring_buffer):
    """Week 2: Check empty buffer, invalid orders, and full buffer."""

    print("\nWEEK 2 IPC CHECKS")
    print("-" * 55)

    # Test 1: Empty buffer
    if ring_buffer.read_order() is None:
        print("PASS: Empty buffer handled correctly.")
    else:
        raise RuntimeError("Empty-buffer check failed.")

    # Test 2: Invalid order
    try:
        ring_buffer.write_order(0, 100_000, 1)
    except ValueError:
        print("PASS: Invalid order rejected correctly.")
    else:
        raise RuntimeError(
            "Invalid-order check failed. Check ring_buffer.py validation."
        )

    # Test 3: Fill buffer to capacity
    for order_id in range(1, ring_buffer.capacity + 1):
        if not ring_buffer.write_order(order_id, 100_000, 1):
            raise RuntimeError("Buffer filled earlier than expected.")

    # One extra order must not be accepted
    if ring_buffer.write_order(
        ring_buffer.capacity + 1, 100_000, 1
    ):
        raise RuntimeError("Full-buffer check failed.")

    print("PASS: Full buffer safely refused an extra order.")

    # Empty the buffer before the main simulation
    for _ in range(ring_buffer.capacity):
        if ring_buffer.read_order() is None:
            raise RuntimeError("Buffer recovery check failed.")

    if not ring_buffer.is_empty():
        raise RuntimeError("Buffer was not empty after recovery.")

    print("PASS: Buffer recovered successfully.")


async def consume_orders(ring_buffer, producer_task, state):
    """Week 1: Consume and verify generated orders."""

    consumed = 0
    checksum = 0

    while not producer_task.done() or not ring_buffer.is_empty():
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
    print("       CHRONOSMATCH - WEEK 1 + WEEK 2")
    print("=" * 55)

    ring_buffer = RingBuffer()

    try:
        # Run Week 2 error-handling checks first
        run_ipc_checks(ring_buffer)

        # Week 1 producer-consumer simulation
        simulator = MarketSimulator(
            ring_buffer=ring_buffer,
            total_orders=TOTAL_ORDERS,
        )

        consumer_state = {}
        start_time = time.perf_counter()

        producer_task = asyncio.create_task(
            simulator.generate_orders()
        )

        consumer_task = asyncio.create_task(
            consume_orders(
                ring_buffer,
                producer_task,
                consumer_state,
            )
        )

        producer_result, _ = await asyncio.gather(
            producer_task,
            consumer_task,
        )

        total_elapsed = time.perf_counter() - start_time

        consumed = consumer_state["consumed"]
        checksum = consumer_state["checksum"]
        expected_checksum = TOTAL_ORDERS * (TOTAL_ORDERS + 1) // 2

        print("\nWEEK 1 + WEEK 2 RESULTS")
        print("-" * 55)
        print(f"Orders requested: {TOTAL_ORDERS}")
        print(f"Orders successfully generated: {producer_result['generated']}")
        print(f"Orders failed: {producer_result['failed']}")
        print(f"Orders rejected: {producer_result.get('rejected', 0)}")
        print(f"Orders consumed: {consumed}")
        print(f"Order ID checksum: {checksum}")

        print(
            f"Producer elapsed time: "
            f"{producer_result['elapsed_seconds']:.4f} seconds"
        )
        print(f"Total elapsed time: {total_elapsed:.4f} seconds")

        if total_elapsed > 0:
            print(
                f"End-to-end throughput: "
                f"{consumed / total_elapsed:.2f} orders/second"
            )

        print("\nFINAL VALIDATION")
        print("-" * 55)

        passed = (
            producer_result["generated"] == TOTAL_ORDERS
            and producer_result["failed"] == 0
            and producer_result.get("rejected", 0) == 0
            and consumed == TOTAL_ORDERS
            and checksum == expected_checksum
            and ring_buffer.is_empty()
        )

        if passed:
            print("PASS: All orders were transferred and verified.")
            print("PASS: Week 2 IPC checks passed.")
        else:
            print("FAIL: One or more checks failed.")

    finally:
        ring_buffer.close()

    print("\nChronosMatch prototype finished.")


if __name__ == "__main__":
    asyncio.run(main())




