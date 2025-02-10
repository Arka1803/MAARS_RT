import os
import argparse
import glob
# import pandas as pd
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
import ast
import numpy as np


def process_file(file_name, output_folder, summary_data, file_count, victim_id, attacker_id):
    

    # Split and extract utilization and no.of tasks
    parts = file_name.replace(".txt", "").split("_")
    u_r = parts[2] 
    n_t = int(parts[4])  
    values_list = [parts[2], int(parts[4])]

    global p_list_index
    attacker = [attacker_id]  # Default attacker ID
    victim = [victim_id]  # Default victim ID
    
    # Construct task set file path
    task_file_name = file_name.replace("schedule_", "task_set_")
    task_file_path = os.path.join("..\\data\\task_set", task_file_name)

    try:
        with open(task_file_path, 'r') as f:
            lines = f.readlines()
        task_set = [tuple(map(int, line.split())) for line in lines]
        
        # Check if victim ID is within range
        if victim[0] < 1 or victim[0] > len(task_set):
            raise ValueError(f"Victim ID {victim[0]} is out of range (1-{len(task_set)})")
        
        victim_sampling_rate = task_set[victim[0] - 1][0]  # Extract period based on ID
        victim_execution_time = task_set[victim[0] - 1][1]  # Extract execution time based on ID
        attacker_sampling_rate= task_set[attacker[0] - 1][0]
        attacker_execution_time= task_set[attacker[0] - 1][1]
        
    except FileNotFoundError:
        print(f"Error: Task set file '{task_file_path}' not found.")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None
    
    # AEW length
    posterior_AEW = 20
    P_list = []
    
    # Define file paths
    read_file_path = os.path.join("..\\data\\schedules", file_name)
    output_file_path = os.path.join(output_folder, f'P_{file_name}.csv')
    
    try:
        with open(read_file_path, 'r') as schedule_file, open(output_file_path, "w") as file:
            for line in schedule_file:
                schedule_sequence = [int(task) for task in line.strip()[1:-1].split()]
                posterior_counter = [0] * len(attacker)
                
                for i, attack_task in enumerate(attacker):
                    attack_indices = [index for index, task in enumerate(schedule_sequence) if task == attack_task]
                    for j, victim_task in enumerate(victim):
                        victim_indices = [index for index, task in enumerate(schedule_sequence) if task == victim_task]
                        
                        # Check if any victim task comes after the attack task within the posterior AEW
                        for attack_index in attack_indices:
                            if any(victim_index > attack_index and victim_index <= attack_index + posterior_AEW for victim_index in victim_indices):
                                posterior_counter[i] += 1
                
                P_C = sum(posterior_counter) / len(schedule_sequence)*attacker_execution_time #* (victim_sampling_rate / victim_execution_time)+ global_list[global_list_index]
                P_list.append(P_C)
                file.write(f"{P_C}\n")
        


        # Compute and return the average probability
        if P_list:
            avg_p = sum(P_list) / len(P_list)
            # Add value from global list based on index
            avg_p += p_list[p_list_index]
            summary_data.append((values_list, avg_p))  # Store for final CSV
        
            # Increment index every 6 files
            if (file_count + 1) % 6 == 0:
                p_list_index = (p_list_index + 1) % len(p_list)
            
            return avg_p
        else:
            print(f"No valid probability values for {file_name}.")
            return None
    except FileNotFoundError:
        print(f"Error: Schedule file '{read_file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return None
p_list = [0.14, 0.24, 0.26, 0.38, 0.26] #initial Prob. observations of task 
p_list_index = 0                         #[V-1,A-4], will change according to attacker-victim combo

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', type=str, default="..\\data\\schedules", help="Folder containing schedule files")
    parser.add_argument('--output_folder', type=str, default="..\\data\\attack_probability", help="Folder to save probability CSVs")
    parser.add_argument('--summary_file', type=str, default="..\\data\\attack_probability\\summary.csv", help="CSV file to save all average probabilities")
    parser.add_argument('--v_i', type=int, default =1 ,help='Victim ID (1-based index)')
    parser.add_argument('--a_i', type=int, default =4 ,help='Attacker ID')
    args = parser.parse_args()


    victim_id = args.v_i  # Default victim ID
    attacker_id= args.a_i


    os.makedirs(args.output_folder, exist_ok=True)
    schedule_files = glob.glob(os.path.join(args.input_folder, "schedule_*.txt"))
    
    if not schedule_files:
        print("No schedule files found in the input folder.")
        return
    
    summary_data = []
    
    for i, file_path in enumerate(schedule_files):
        file_name = os.path.basename(file_path)
        process_file(file_name, args.output_folder, summary_data, i, victim_id, attacker_id)
    
    summary_file_path = args.summary_file
    with open(summary_file_path, "w") as summary_file:
        summary_file.write("[util,task_no], Average Probability\n")
        for file_name, avg_p in summary_data:
            
            summary_file.write(f"{file_name},{avg_p:.6f}\n")
    
    print(f"\nSummary of all average probabilities saved in: {summary_file_path}")

#Start Plotting 

#Open file in Read Mode
if __name__ == "__main__":
    main()

    util_ranges = []
    task_numbers = []
    avg_ap_values = []

    # Read the file and process each row
    with open('..\\data\\attack_probability\\summary.csv', 'r') as file:
        next(file)  # Skip header
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('],')
            if len(parts) != 2:
                continue
            
            util_task_part = parts[0].strip('[]')
            avg_ap = float(parts[1].strip())
            
            util_range, task_no = util_task_part.split(", ")
            util_ranges.append(util_range.strip("'"))
            task_numbers.append(int(task_no))
            avg_ap_values.append(avg_ap)

    # Organize data by unique task numbers
    data = {}
    for util, task, ap in zip(util_ranges, task_numbers, avg_ap_values):
        if task not in data:
            data[task] = {'util': [], 'ap': []}
        data[task]['util'].append(util)
        data[task]['ap'].append(ap)

    # Sort utilization groups for proper plotting
    util_order = sorted(set(util_ranges), key=lambda x: float(x.split('-')[0]))

    # Plot the data
    plt.figure(figsize=(10, 6))

    for task_no, values in data.items():
        sorted_pairs = sorted(zip(values['util'], values['ap']), key=lambda x: util_order.index(x[0]))
        sorted_util, sorted_ap = zip(*sorted_pairs)
        plt.plot(sorted_util, sorted_ap, marker='o', linestyle='-', label=f'Task {task_no}')

    plt.xlabel('Utilization Group')
    plt.ylabel('Average Probability')
    plt.title('Average AP vs Utilization Group')
    plt.legend()
    plt.ylim([0,1])
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

    
    




