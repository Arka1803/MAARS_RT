import heapq

# Define a Task class to hold task information
class Task:
    def __init__(self, priority, period, execution_time):
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.deadline = period  
        self.remaining_time = execution_time

    def __lt__(self, other):
       
        return self.priority < other.priority

# Function to schedule tasks using a preemptive fixed-priority policy
def schedule_tasks(tasks, hyperperiod):
    current_time = 0
    task_queue = []
    scheduled_tasks = []

    while current_time < hyperperiod:
        task_executed = False  

        # Check if any tasks have arrived
        for task in tasks:
            if current_time % task.period == 0:
                heapq.heappush(task_queue, task)

        if task_queue:
            # Get the highest priority task from the queue
            current_task = heapq.heappop(task_queue)

           
            current_task.remaining_time -= 1
            scheduled_tasks.append(current_task.priority) 
            task_executed = True

            # Check if the task is completed
            if current_task.remaining_time == 0:
                # Reset remaining time and calculate next arrival time
                current_task.remaining_time = current_task.execution_time

        if not task_executed:
            scheduled_tasks.append(0)

        current_time += 1

    return scheduled_tasks

# Example tasks

tasks = [
    Task(priority=1, period=10, execution_time=1),
    Task(priority=2, period=10, execution_time=1),
    Task(priority=3, period=10, execution_time=1),
    Task(priority=4, period=20, execution_time=1),
    Task(priority=5, period=10, execution_time=1),
    Task(priority=6, period=30, execution_time=1),
    Task(priority=7, period=20, execution_time=1)
]


# Calculate the hyperperiod (LCM of task periods)
from math import lcm
hyperperiod = lcm(*[task.period for task in tasks])

# Schedule the tasks
scheduled_tasks = schedule_tasks(tasks, hyperperiod)

# Print the scheduled task sequence
print("Scheduled Task Sequence:")
print(scheduled_tasks)