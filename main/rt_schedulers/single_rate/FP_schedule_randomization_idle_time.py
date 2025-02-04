import random
from math import lcm
import os

# Define a Task class to hold task information
class Task:
    def __init__(self, priority, period, execution_time):
        self.priority = priority
        self.period = period
        self.execution_time = execution_time

# Function to schedule tasks using a preemptive fixed-priority policy
def schedule_tasks(tasks, hyperperiod):
    current_time = 0
    scheduled_tasks = []

    while current_time < hyperperiod:
        tasks_in_period = []

        # Check if any tasks have arrived
        for task in tasks:
            if current_time % task.period == 0:
                tasks_in_period.extend([task.priority] * task.execution_time)

        if tasks_in_period:
            # Shuffle tasks within the period while maintaining their relative order
            random.shuffle(tasks_in_period)

            # Append shuffled tasks to the schedule
            scheduled_tasks.extend(tasks_in_period)

        else:
            # If no tasks arrived in the period, append idle time
            scheduled_tasks.append(0)

        current_time += 1

    # Ensure schedule length matches hyperperiod length by adding idle times if necessary
    while len(scheduled_tasks) < hyperperiod:
        scheduled_tasks.append(0)

    # Shuffle the schedule again to intersperse idle times randomly
    random.shuffle(scheduled_tasks)

    return scheduled_tasks

# Example tasks
tasks = [
    Task(priority=1, period=10, execution_time=1),
    Task(priority=2, period=10, execution_time=1),
    Task(priority=3, period=10, execution_time=1),
    Task(priority=4, period=20, execution_time=1),
    Task(priority=5, period=10, execution_time=1),
    Task(priority=6, period=30, execution_time=1),
    Task(priority=7, period=25, execution_time=1),
    Task(priority=8, period=30, execution_time=5),
    Task(priority=9, period=10, execution_time=2),
]

# Calculate the hyperperiod (LCM of task periods)
hyperperiod = lcm(*[task.period for task in tasks])

# Number of random schedules to generate
num_random_schedules = 660  # Adjust as needed

# Define the full path where the file should be saved
folder_path = "main\data\schedules\FP_schedule_randomization_idle_time"  # Absolute path

# Ensure the folder exists, create it if necessary
os.makedirs(folder_path, exist_ok=True)

# Define the full path of the output file
file_path = os.path.join(folder_path, "idle_time_fp_schedules.txt")

# Write schedules to the specified folder and file
with open(file_path, "w") as file:
    for i in range(num_random_schedules):
        scheduled_tasks = schedule_tasks(tasks, hyperperiod)
        file.write("[ ")
        file.write(" ".join(map(str, scheduled_tasks[:hyperperiod])))  # Write only up to hyperperiod length
        file.write(" ]\n")

print(f"Total random schedules generated: {num_random_schedules}")
print(f"Schedules saved to: {file_path}")
