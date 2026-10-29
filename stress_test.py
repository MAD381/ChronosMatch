
from performance_test import run_transfer_test


async def run_stress_tests():
    """Run repeated stress tests and return True if all pass."""

    test_sizes = [10_000, 50_000, 100_000]
    repetitions = 3

    total_tests = 0
    passed_tests = 0

    for size in test_sizes:
        print(f"\nTesting {size:,} orders")

        for attempt in range(1, repetitions + 1):
            total_tests += 1

            try:
                result = await run_transfer_test(
                    size,
                    f"WEEK 4: Stress test {attempt}/{repetitions}",
                )

                if result["passed"]:
                    passed_tests += 1

                print(
                    f"Run {attempt}: "
                    f"{'PASS' if result['passed'] else 'FAIL'}"
                )

            except Exception as error:
                print(f"Run {attempt}: ERROR - {error}")

    print("\nWEEK 4 STRESS TEST SUMMARY")
    print("-" * 55)
    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {total_tests - passed_tests}")

    return passed_tests == total_tests
