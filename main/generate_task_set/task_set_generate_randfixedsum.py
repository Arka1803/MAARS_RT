import os
import numpy as np
import random
from math import gcd
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
    Generate n random numbers that sum to u using the RandfixedSum algorithm.
    
    Parameters:
    - n (int): Number of random numbers.
    - u (float): The sum of the random numbers.
    
    Returns:
    - np.ndarray: Array containing the generated numbers.
    """
    if n < 1:
        return np.array([])

    if n == 1:
        return np.array([u])

    # Generate random numbers that sum up to 1
    v = np.sort(np.random.rand(n - 1))
    x = np.zeros(n)
    x[0] = v[0]
    for i in range(1, n - 1):
        x[i] = v[i] - v[i - 1]
    x[-1] = 1 - v[-1]
    
    # Scale the random numbers to sum up to u
    x = x * u
    return x

def generate_task_set(utilization, num_tasks, hyperperiod_divisors):
    """
    Generate a task set with a given utilization using the RandfixedSum algorithm.
    
    Parameters:
    - utilization (float): Desired total utilization of the task set.
    - num_tasks (int): Number of tasks in the task set.
    - hyperperiod_divisors (list): List of possible periods (divisors of hyperperiod).
    
    Returns:
    - list: A list of tuples representing the task set (period, execution time).
    """
    task_set = []
    utilizations = randfixedsum(num_tasks, utilization)
    
    for util in utilizations:
        period = random.choice(hyperperiod_divisors)  # Choose period from hyperperiod divisors
        execution_time = max(1, round(period * util))  # Ensure execution time is at least 1
        task_set.append((period, execution_time))
    
    return task_set

def save_task_set_to_file(task_set, filename):
    """
    Save the generated task set to a file in the specified directory.
    
    Parameters:
    - task_set (list): The generated task set.
    - filename (str): The file name to save the task set.
    """
    output_dir = "main\\data\\task_set"   # Define the full path to the target folder and file name
    
    # Ensure the directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_path = os.path.join(output_dir, filename)
    
    # Write the task set to the file
    with open(file_path, 'w') as file:
        for period, execution_time in task_set:
            file.write(f"{period} {execution_time}\n")
    
    print(f"Task set saved to {file_path}")

def main():
    # Get user input
    utilization_ranges = input("Enter desired utilization ranges separated by commas (e.g., 0.2-0.4,0.5-0.6): ")
    task_counts = list(map(int, input("Enter number of tasks separated by commas (e.g., 5,10,15): ").split(',')))
    hyperperiod = int(input("Enter hyperperiod: "))

    # Parse utilization ranges
    ranges = [tuple(map(float, r.split('-'))) for r in utilization_ranges.split(',')]
    
    # Validate utilization ranges
    for min_util, max_util in ranges:
        if min_util < 0 or max_util > 1 or min_util >= max_util:
            print(f"Invalid utilization range: {min_util}-{max_util}. Please enter values where min < max and between 0 and 1.")
            return
    
    if any(count <= 0 for count in task_counts):
        print("Invalid number of tasks. Please enter positive integers.")
        return
    
    # Compute hyperperiod divisors
    hyperperiod_divisors = get_divisors(hyperperiod)
    
    # Generate task sets for all combinations of utilization ranges and task counts
    for min_util, max_util in ranges:
        for num_tasks in task_counts:
            total_utilization = random.uniform(min_util, max_util)
            task_set = generate_task_set(total_utilization, num_tasks, hyperperiod_divisors)
            filename = f"task_set_util_{min_util}-{max_util}_tasks_{num_tasks}.txt"
            save_task_set_to_file(task_set, filename)

if __name__ == "__main__":
    main()
