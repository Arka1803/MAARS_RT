import csv
import os
import argparse

def read_schedules(filename):
    schedules = []
    with open(filename, 'r') as file:
        lines = file.readlines()[::1]  # Skip every alternate line
        for line in lines:
            schedule_str = line.strip()[1:-1]  # Remove brackets
            schedule = list(map(int, schedule_str.split()))
            schedules.append(schedule)
    return schedules

def calculate_inference_ratio(schedule, attacker_id, victim_id, sampling_period):
    schedule_length = len(schedule)
    num_parts = schedule_length // sampling_period
    total_preemptions_count = 0
    unique_columns = set()
    
    for i in range(num_parts):
        part_start = i * sampling_period
        part_schedule = schedule[part_start:part_start + sampling_period]
        
        # Count preemptions: Attacker immediately following victim
        preemptions_count = sum(
            1 for j in range(len(part_schedule) - 1)
            if part_schedule[j] == victim_id and part_schedule[j + 1] == attacker_id
        )
        
        total_preemptions_count += preemptions_count

        # Track unique arrival instances of attacker
        unique_columns.update(j for j, task in enumerate(part_schedule) if task == attacker_id)
    
    total_arrival_count = len(unique_columns)

    # Debugging Output
    print(f"Total Preemptions Count: {total_preemptions_count}")
    print(f"Unique Arrival Count: {total_arrival_count}")

    # Calculate Inference Ratio (IR)
    IR = total_preemptions_count / total_arrival_count if total_arrival_count > 0 else 0

    return IR

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='File name to take as input')
    parser.add_argument('--v_i', type=int, default=1, help='Victim ID (default: 1)')
    parser.add_argument('--v_p', type=int, default=16, help='Victim period (default: 16)')
    parser.add_argument('--a_i', type=int, default=4, help='Attacker ID (default: 4)')
    args = parser.parse_args()
    
    # Assign parsed arguments
    attacker_id = args.a_i
    victim_id = args.v_i
    sampling_period = args.v_p

    # Define paths
    out_path = os.path.join("..", "data", "inferability_ratio")
    os.makedirs(out_path, exist_ok=True)

    filename = os.path.join(out_path, f'IR_{args.file_name}.csv')
    input_file_path = os.path.join("..", "data", "schedules", args.file_name)

    # Check if the file exists to determine write mode
    mode = 'a' if os.path.isfile(filename) else 'w'

    schedules = read_schedules(input_file_path)
    
    with open(filename, mode, newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        
        if mode == 'w':
            writer.writerow(['Schedule', 'Inference Ratio'])
        
        for idx, schedule in enumerate(schedules):
            inference_ratio = calculate_inference_ratio(schedule, attacker_id, victim_id, sampling_period)
            writer.writerow([f"Schedule {idx+1}", inference_ratio])
