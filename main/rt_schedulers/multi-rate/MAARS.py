import heapq
import random
import itertools
from math import lcm
import os

# Define a Task class 
class Task:
    def __init__(self, task_id, priority, periods, execution_time):
        self.task_id = task_id
        self.priority = priority
        self.periods = periods
        self.execution_time = execution_time
        self.deadline = periods[0]  
        self.remaining_time = execution_time

    def __lt__(self, other):
        
        return self.priority < other.priority


def schedule_tasks(tasks, hyperperiod):
    current_time = 0
    task_queue = []
    scheduled_tasks = []

    while current_time < hyperperiod:
        task_executed = False  

        # Check if any tasks have arrived
        for task in tasks:
            if current_time % task.periods[0] == 0:
                heapq.heappush(task_queue, task)

        if task_queue:
            
            random.shuffle(task_queue)

            
            current_task = heapq.heappop(task_queue)

            # Execute the task for one time unit
            current_task.remaining_time -= 1
            scheduled_tasks.append(current_task.task_id)  # Append task ID
            task_executed = True

            # Check if the task is completed
            if current_task.remaining_time == 0:
                
                current_task.remaining_time = current_task.execution_time

        if not task_executed:
            
            scheduled_tasks.append(0)

        current_time += 1

    return scheduled_tasks

# Example tasks with unique task IDs
tasks = [
    Task(task_id=1, priority=1, periods=[10,60], execution_time=1),
    Task(task_id=2, priority=2, periods=[4,10], execution_time=1),
    Task(task_id=3, priority=3, periods=[60,120], execution_time=3),
    Task(task_id=4, priority=4, periods=[25,150], execution_time=1),
    Task(task_id=5, priority=5, periods=[60,100], execution_time=20),
]

# Generate all possible permutations of task periods
period_permutations = []
for task in tasks:
    period_permutations.append(itertools.permutations(task.periods, len(task.periods)))

# Define the folder path where the file should be saved
folder_path = "main\data\schedules\MAARS"  

# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "MAARS_schedules.txt")

# Open a file in write mode
with open(file_path, 'w') as f:
    total_schedules = 0
    for period_permutation in itertools.product(*period_permutations):
        for task, periods in zip(tasks, period_permutation):
            task.periods = periods  # Update task periods
        hyperperiod = lcm(*[task.periods[0] for task in tasks])  # Calculate hyperperiod based on current schedules
        scheduled_tasks = schedule_tasks(tasks, hyperperiod)
        total_schedules += 1
        # Write the generated sequence without commas (space-separated)
        f.write("[ ")
        f.write(" ".join(map(str, scheduled_tasks)))
        f.write(" ]\n")
# Optionally write the total number of schedules generated to the file
# f.write(f"Total schedules generated: {total_schedules}\n")        

print(f"Total schedules generated: {total_schedules}")
print(f"Schedules saved to: {file_path}")
