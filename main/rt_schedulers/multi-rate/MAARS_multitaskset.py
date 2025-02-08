import heapq
import random
import itertools
from math import lcm
import os
import re

# Define the Task class
class Task:
    def __init__(self, task_id, priority, periods, execution_time):
        self.task_id = task_id
        self.priority = priority
        self.periods = periods
        self.execution_time = execution_time
        self.deadline = periods[0]  # Assuming the first period is the deadline
        self.remaining_time = execution_time

    def __lt__(self, other):
        return self.priority < other.priority

# Read tasks from the file
def read_task_file(file_path):
    tasks = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        period, execution_time = map(int, line.split())
        tasks.append(Task(task_id=i + 1, priority=i + 1, periods=[period, period*2, period*3], execution_time=execution_time))
    return tasks

# Scheduling tasks based on permutations of periods
def schedule_tasks(tasks, hyperperiod):
    current_time = 0
    task_queue = []
    scheduled_tasks = []

    while current_time < hyperperiod:
        task_executed = False

        # Check if any tasks have arrived
        for task in tasks:
            if current_time % task.periods[current_time % len(task.periods)] == 0:  
                heapq.heappush(task_queue, task)

        if task_queue:
            random.shuffle(task_queue)  # Shuffle between active jobs
            current_task = heapq.heappop(task_queue)
            current_task.remaining_time -= 1
            scheduled_tasks.append(current_task.task_id)
            task_executed = True

            if current_task.remaining_time == 0:
                current_task.remaining_time = current_task.execution_time  # Reset task

        if not task_executed:
            scheduled_tasks.append(0)

        current_time += 1

    return scheduled_tasks

# Process task files and generate schedules, limited to 1000 schedules
def process_task_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_path = os.path.join(input_folder, file_name)
            match = re.match(r"task_set_util_(.*)_tasks_(\d+)\.txt", file_name)
            if not match:
                continue
            util_range, num_tasks = match.groups()
            output_file = os.path.join(output_folder, f"schedule_util_{util_range}_tasks_{num_tasks}.txt")

            tasks = read_task_file(input_path)
            period_permutations = [itertools.permutations(task.periods) for task in tasks]  # All permutations for each task
            total_schedules = 0

            with open(output_file, 'w') as f:
                for period_permutation in itertools.product(*period_permutations):
                    # if total_schedules >= 100:  # Stop once 1000 schedules are written
                    #     break
                    for task, periods in zip(tasks, period_permutation):
                        task.periods = periods  # Set permuted periods to task
                    # Calculate hyperperiod based on all permuted periods
                    hyperperiod = lcm(*[period[0] for period in period_permutation])
                    scheduled_tasks = schedule_tasks(tasks, hyperperiod)
                    total_schedules += 1
                    f.write("[ " + " ".join(map(str, scheduled_tasks)) + " ]\n")
                    if total_schedules >= 100:  # Stop if we've written 1000 schedules
                        break

            print(f"Processed {file_name}: {total_schedules} schedules saved to {output_file}")

# Example usage:
input_folder = "main\\data\\task_set"
output_folder = "main\\data\\schedules"
process_task_files(input_folder, output_folder)
