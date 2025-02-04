import heapq
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Define a Task class to hold task information
class Task:
    def __init__(self, task_id, priority, period, execution_time):
        self.task_id = task_id
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.deadline = period  # Assuming deadline is equal to period
        self.remaining_time = execution_time

    def __lt__(self, other):
        # Define the comparison for the priority queue
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
            # Randomize the order of tasks within the queue for each time unit
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
    Task(task_id=1, priority=2, period=10, execution_time=2),
    Task(task_id=2, priority=1, period=5, execution_time=1),
    Task(task_id=3, priority=3, period=15, execution_time=3),
]

# Calculate the hyperperiod (LCM of task periods)
from math import lcm
hyperperiod = lcm(*[task.period for task in tasks])

# Number of random schedules to generate
num_random_schedules = 15  # Adjust as needed

# Assign unique colors to tasks
task_colors = {
    1: "blue",
    2: "red",
    3: "green",
}

# Reduce the height of the boxes (adjust as needed)
box_height = 0.4

# Define the number of rows and columns for subplots
num_rows = 4
num_cols = 5

# Create subplots for displaying schedules
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 16))
fig.subplots_adjust(hspace=0.5)

# Generate and display random schedules
for i in range(num_random_schedules):
    random.seed(i)  
    scheduled_tasks = schedule_tasks(tasks, hyperperiod)

    row = i // num_cols
    col = i % num_cols

    # Draw rectangles 
    for t, task_id in enumerate(scheduled_tasks):
        if task_id == 0:
            color = "white"
        else:
            color = task_colors[task_id]
        rect = Rectangle((t, 0), 1, box_height, color=color, edgecolor='black')
        axes[row, col].add_patch(rect)

    # Add borders between time units
    for t in range(hyperperiod):
        axes[row, col].axvline(x=t, color='black', linewidth=0.5)

    # Set x-axis and y-axis labels
    axes[row, col].set_xlabel('Time')
    axes[row, col].set_ylabel('Schedule')
    axes[row, col].set_title(f'Schedule {i + 1}')

# Remove empty subplots
for i in range(num_random_schedules, num_rows * num_cols):
    row = i // num_cols
    col = i % num_cols
    fig.delaxes(axes[row, col])

# Display the figure
plt.show()

print(f"Total random schedules generated: {num_random_schedules}")