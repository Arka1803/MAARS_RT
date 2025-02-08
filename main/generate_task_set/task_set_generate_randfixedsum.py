import numpy as np
import random
import os
from math import gcd, ceil
from functools import reduce

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def compute_hyperperiod(periods):
    return reduce(lcm, periods, 1)

def get_divisors(n):
    """Return a list of divisors of n."""
    divisors = [i for i in range(1, n + 1) if n % i == 0]
    return divisors

def randfixedsum(n, u):
    """
    Generate `n` random values that sum to `u`.
    """
    if n == 1:
        return np.array([u])

    # Generate random values that sum up to `u`
    v = np.sort(np.random.rand(n - 1))
    x = np.zeros(n)
    x[0] = v[0]
    for i in range(1, n - 1):
        x[i] = v[i] - v[i - 1]
    x[-1] = 1 - v[-1]

    # Scale values to sum to `u`
    return x * u

def generate_task_set(utilization, num_tasks, hyperperiod_divisors):
    """
    Generate a task set with a given utilization.

    Parameters:
    - utilization (float): Total desired utilization.
    - num_tasks (int): Number of tasks.
    - hyperperiod_divisors (list): Possible periods.

    Returns:
    - list: List of (period, execution time).
    """
    task_set = []
    utilizations = randfixedsum(num_tasks, utilization)  # Generate utilizations

    for util in utilizations:
        period = random.choice(hyperperiod_divisors)  # Choose period
        execution_time = max(1, ceil(period * util))  # Ensure execution time is at least 1
        
        # Adjust execution time if total utilization is mismatched
        actual_util = execution_time / period
        if actual_util > util and execution_time > 1:
            execution_time -= 1  # Reduce to maintain sum

        task_set.append((period, execution_time))
    
    return task_set

def save_task_set_to_file(task_set, filename):
    """
    Save the generated task set to a file.
    """
    output_dir = "main\\data\\task_set"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w') as file:
        for period, execution_time in task_set:
            file.write(f"{period} {execution_time}\n")
    
    print(f"Task set saved to {file_path}")

def main():
    utilization_ranges = input("Enter utilization ranges (e.g., 0.2-0.4,0.5-0.6): ")
    task_counts = list(map(int, input("Enter task counts (e.g., 5,10,15): ").split(',')))
    hyperperiod = int(input("Enter hyperperiod: "))

    ranges = [tuple(map(float, r.split('-'))) for r in utilization_ranges.split(',')]

    for min_util, max_util in ranges:
        for num_tasks in task_counts:
            total_utilization = random.uniform(min_util, max_util)
            hyperperiod_divisors = get_divisors(hyperperiod)
            task_set = generate_task_set(total_utilization, num_tasks, hyperperiod_divisors)
            filename = f"task_set_util_{min_util}-{max_util}_tasks_{num_tasks}.txt"
            save_task_set_to_file(task_set, filename)

if __name__ == "__main__":
    main()
