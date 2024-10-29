#!/bin/python3

from utils import generate_prime_pair
import time

start_time = time.perf_counter()
generate_prime_pair(3000)
end_time = time.perf_counter()

execution_time_ms = (end_time - start_time) * 1000
print(f"Execution time: {execution_time_ms:.4f} ms")
