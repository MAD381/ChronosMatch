
# Import the function used to perform order transfer and performance testing.
from performance_test import run_transfer_test


# Define an asynchronous function to run repeated stress tests.
async def run_stress_tests():
    """Run repeated stress tests and return True if all tests pass."""

    # Define the different order volumes for stress testing.
    test_sizes = [10_000, 50_000, 100_000]

    # Repeat each test size three times to check system stability.
    repetitions = 3

    # Initialize counters to track total and successful tests.
    total_tests = 0
    passed_tests = 0

    # Run stress tests for each specified order volume.
    for size in test_sizes:
        print(f"\nTesting {size:,} orders")

        # Repeat the test for the current order volume.
        for attempt in range(1, repetitions + 1):
            total_tests += 1

            try:
                # Execute the order transfer test and collect its result.
                result = await run_transfer_test(
                    size,
                    f"WEEK 4: Stress test {attempt}/{repetitions}",
                )

                # Increase the successful test counter if the test passes.
                if result["passed"]:
                    passed_tests += 1

                # Display whether the current test passed or failed.
                print(f"Run {attempt}: " f"{'PASS' if result['passed'] else 'FAIL'}")

            except Exception as error:
                # Handle unexpected errors without stopping the remaining tests.
                print(f"Run {attempt}: ERROR - {error}")

    # Display the final stress testing summary.
    print("\nWEEK 4 STRESS TEST SUMMARY")
    print("-" * 55)
    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {total_tests - passed_tests}")

    # Return True only when every test has passed.
    return passed_tests == total_tests
