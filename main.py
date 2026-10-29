
import asyncio

from config import TOTAL_ORDERS
from performance_test import run_transfer_test
from stress_test import run_stress_tests
from ring_buffer import RingBuffer


def run_week2_checks():
    """Run the Week 2 input-validation and buffer checks."""

    buffer = RingBuffer()
    passed = True

    try:
        print("\nWEEK 2: IPC AND ERROR-HANDLING CHECKS")
        print("-" * 55)

        if buffer.read_order() is None:
            print("PASS: Empty buffer handled correctly.")
        else:
            print("FAIL: Empty-buffer check.")
            passed = False

        try:
            buffer.write_order(0, 100000, 1)
        except ValueError:
            print("PASS: Invalid order rejected correctly.")
        else:
            print("FAIL: Invalid order was accepted.")
            passed = False

        for order_id in range(1, buffer.capacity + 1):
            if not buffer.write_order(order_id, 100000, 1):
                print("FAIL: Buffer filled earlier than expected.")
                passed = False
                break

        if buffer.is_full():
            print("PASS: Buffer reached its capacity.")
        else:
            print("FAIL: Buffer did not reach capacity.")
            passed = False

        if buffer.write_order(buffer.capacity + 1, 100000, 1) is False:
            print("PASS: Full buffer refused an extra order.")
        else:
            print("FAIL: Full buffer accepted an extra order.")
            passed = False

        for _ in range(buffer.capacity):
            if buffer.read_order() is None:
                print("FAIL: Buffer recovery failed.")
                passed = False
                break

        if buffer.is_empty():
            print("PASS: Buffer recovered successfully.")
        else:
            print("FAIL: Buffer was not empty after recovery.")
            passed = False

    finally:
        buffer.close()

    return passed


async def main():
    print("=" * 60)
    print("CHRONOSMATCH - COMPLETE WEEK 1 TO WEEK 4")
    print("=" * 60)

    # WEEK 1: Main order-transfer test
    week1_result = await run_transfer_test(
        TOTAL_ORDERS,
        "WEEK 1: ORDER TRANSFER",
    )
    week1_passed = week1_result["passed"]

    # WEEK 2: Buffer and input validation
    week2_passed = run_week2_checks()

    # WEEK 3: Performance test with a high order volume
    week3_result = await run_transfer_test(
        TOTAL_ORDERS,
        "WEEK 3: PERFORMANCE TEST",
    )
    week3_passed = week3_result["passed"]

    # WEEK 4: Repeated stability and stress tests
    week4_passed = await run_stress_tests()

    # FINAL SUMMARY
    print("\n" + "=" * 60)
    print("FINAL SUMMARY - ALL FOUR WEEKS")
    print("=" * 60)
    print(f"Week 1 - Order transfer: {'PASS' if week1_passed else 'FAIL'}")
    print(f"Week 2 - Validation: {'PASS' if week2_passed else 'FAIL'}")
    print(f"Week 3 - Performance: {'PASS' if week3_passed else 'FAIL'}")
    print(f"Week 4 - Stress testing: {'PASS' if week4_passed else 'FAIL'}")

    overall_passed = (
        week1_passed
        and week2_passed
        and week3_passed
        and week4_passed
    )

    print("-" * 60)
    print(f"OVERALL RESULT: {'PASS' if overall_passed else 'FAIL'}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
