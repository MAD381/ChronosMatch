import asyncio
import subprocess
import sys

from config import TOTAL_ORDERS
from performance_test import run_transfer_test
from stress_test import run_stress_tests
from ring_buffer import RingBuffer


def run_week2_checks():
    """Run Week 2 input-validation and buffer checks."""

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


def run_ai_stock_intelligence():
    """Run all twelve AI Stock Intelligence modules."""

    modules = [
        # Modules 1-7: Existing modules
        (
            "Module 1: Stock Data Collection",
            "ai_stock_intelligence.data_collector",
        ),
        (
            "Module 2: Technical Analysis",
            "ai_stock_intelligence.technical_analysis",
        ),
        (
            "Module 3: AI Stock Prediction",
            "ai_stock_intelligence.stock_predictor",
        ),
        (
            "Module 4: Risk Analysis",
            "ai_stock_intelligence.risk_analyzer",
        ),
        (
            "Module 5: Fundamental Analysis",
            "ai_stock_intelligence.fundamental_analyzer",
        ),
        (
            "Module 6: News Sentiment Analysis",
            "ai_stock_intelligence.news_sentiment",
        ),
        (
            "Module 7: Stock Comparison",
            "ai_stock_intelligence.stock_comparator",
        ),
        # Modules 8-12: Newly added modules
        (
            "Module 8: Portfolio Optimizer",
            "ai_stock_intelligence.portfolio_optimizer",
        ),
        (
            "Module 9: Trading Signal",
            "ai_stock_intelligence.trading_signal",
        ),
        (
            "Module 10: Backtesting Engine",
            "ai_stock_intelligence.backtesting_engine",
        ),
        (
            "Module 11: Portfolio Tracker",
            "ai_stock_intelligence.portfolio_tracker",
        ),
        (
            "Module 12: Interactive Stock Report",
            "ai_stock_intelligence.portfolio_report",
        ),
    ]

    results = []

    print("\n" + "=" * 65)
    print("CHRONOSMATCH - AI STOCK INTELLIGENCE")
    print("RUNNING ALL 12 MODULES")
    print("=" * 65)

    for module_name, module_path in modules:
        print("\n" + "-" * 65)
        print(module_name.upper())
        print("-" * 65)

        try:
            result = subprocess.run(
                [sys.executable, "-m", module_path],
                check=False,
            )

            passed = result.returncode == 0

        except Exception as error:
            print(f"ERROR: {error}")
            passed = False

        results.append((module_name, passed))

        status = "COMPLETED" if passed else "FAILED"
        print(f"\n{module_name}: {status}")

    print("\n" + "=" * 65)
    print("AI STOCK INTELLIGENCE SUMMARY")
    print("=" * 65)

    for module_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{module_name}: {status}")

    print("-" * 65)

    all_passed = all(passed for _, passed in results)

    print("AI MODULE RESULT: " f"{'PASS' if all_passed else 'SOME MODULES FAILED'}")
    print("=" * 65)

    return all_passed


async def main():
    print("=" * 65)
    print("CHRONOSMATCH - COMPLETE WEEK 1 TO WEEK 4")
    print("WITH 12 AI STOCK INTELLIGENCE MODULES")
    print("=" * 65)

    # WEEK 1: Main order-transfer test
    week1_result = await run_transfer_test(
        TOTAL_ORDERS,
        "WEEK 1: ORDER TRANSFER",
    )
    week1_passed = week1_result["passed"]

    # WEEK 2: Buffer and input validation
    week2_passed = run_week2_checks()

    # WEEK 3: Performance test
    week3_result = await run_transfer_test(
        TOTAL_ORDERS,
        "WEEK 3: PERFORMANCE TEST",
    )
    week3_passed = week3_result["passed"]

    # WEEK 4: Stability and stress tests
    week4_passed = await run_stress_tests()

    # AI: Run all twelve stock intelligence modules
    ai_passed = run_ai_stock_intelligence()

    # FINAL SUMMARY
    print("\n" + "=" * 65)
    print("CHRONOSMATCH - COMPLETE PROJECT SUMMARY")
    print("=" * 65)

    print(f"Week 1 - Order transfer: {'PASS' if week1_passed else 'FAIL'}")
    print(f"Week 2 - Validation: {'PASS' if week2_passed else 'FAIL'}")
    print(f"Week 3 - Performance: {'PASS' if week3_passed else 'FAIL'}")
    print(f"Week 4 - Stress testing: {'PASS' if week4_passed else 'FAIL'}")
    print(f"AI Stock Intelligence (12 Modules): " f"{'PASS' if ai_passed else 'FAIL'}")

    overall_passed = (
        week1_passed and week2_passed and week3_passed and week4_passed and ai_passed
    )

    print("-" * 65)
    print(f"OVERALL RESULT: {'PASS' if overall_passed else 'FAIL'}")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(main())
