import csv
import os.path

def read_schedules(filename):
    schedules = []
    with open(filename, 'r') as file:
        lines = file.readlines()[::2]  
        for line in lines:
            schedule_str = line.strip()[1:-1]  
            schedule = list(map(int, schedule_str.split()))
            schedules.append(schedule)
    return schedules

def calculate_inference_ratio(schedule, attacker_id, victim_id, sampling_period):
    # Superimpose the sequences and count arrivals and preemptions for each part
    schedule_length = len(schedule)
    num_parts = schedule_length // sampling_period
    
    total_preemptions_count = 0
    total_arrival_count = 0
    unique_columns = set()
    
    for i in range(num_parts):
        part_start = i * sampling_period
        part_schedule = schedule[part_start:part_start + sampling_period]
        
        # Count preemptions in the current part
        preemptions_count = 0
        for j in range(len(part_schedule)):
            if part_schedule[j] == victim_id:
                for k in range(1, 4):  
                    if j + k < len(part_schedule) and part_schedule[j + k] == attacker_id:
                        preemptions_count += 1
                        break  
        
        total_preemptions_count += preemptions_count
        
        # Track unique columns where the attacker appears
        for j, task in enumerate(part_schedule):
            if task == attacker_id:
                unique_columns.add(j)
    
    total_arrival_count = len(unique_columns)
    
    # Debug print: Preemptions count and arrival count
    print(f"Total Preemptions Count: {total_preemptions_count}")
    print(f"Unique Columns: {unique_columns}")
    print(f"Total Arrival Count: {total_arrival_count}")
    
    # Calculate Inference Ratio (IR)
    if total_arrival_count == 0:  # To avoid division by zero
        IR = 0
    else:
        IR = (total_preemptions_count%total_arrival_count) / sampling_period if total_preemptions_count > 0 else 0
    
    # Debug print: Inference Ratio
    # print(f"Inference Ratio (IR): {IR}")

    return IR

if __name__ == "__main__":


    out_path= "main\data\inferability_ratio"
    os.makedirs(out_path, exist_ok=True)

    # Define the full path for the output CSV file
    filename = os.path.join(out_path, 'maars_ir.csv')

    
    # Read attacker_id, victim_id, and sampling_period as integers
    attacker_id = 5
    victim_id = 1
    sampling_period = 10
  
    path = "main\data\schedules\MAARS"
    input_file_path = os.path.join(path, "MAARS_schedules.txt")


    # Check if the file exists
    if os.path.isfile(filename):
        mode = 'a'  # Append mode
    else:
        mode = 'w'  # Write mode
        
  

    schedules = read_schedules(input_file_path)
    with open(filename, mode, newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        
        # Write header only if the file is newly created
        if mode == 'w':
            writer.writerow(['Schedule', 'Inference Ratio'])
        
        for idx, schedule in enumerate(schedules):
            inference_ratio = calculate_inference_ratio(schedule, attacker_id, victim_id, sampling_period)
            writer.writerow([f"Schedule {idx+1}", inference_ratio])
