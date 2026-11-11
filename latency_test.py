import time

def measure_trade_execution():
    # Start high-precision timer
    start_time = time.perf_counter_ns()
    
    # Simulate a micro-operation or trade matching calculation
    total = sum(i for i in range(10000))
    
    # End timer
    end_time = time.perf_counter_ns()
    
    latency_ns = end_time - start_time
    print(f"Trade Execution Latency: {latency_ns} nanoseconds")
    return latency_ns

if __name__ == "__main__":
    measure_trade_execution()