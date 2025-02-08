import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='File name to take as input')
    parser.add_argument('--v_i', type=int, help='Victim ID')
    parser.add_argument('--v_p', type=int, help='Victim period')
    parser.add_argument('--a_i', type=int, help='Attacker ID (<no. of task)')
    args = parser.parse_args()
    
    # Lists entered by user
    attacker = [args.a_i] if args.a_i is not None else [4]  # Replace with attacker task index
    victim = [args.v_i] if args.v_i is not None else [1]
    victim_sampling_rate = args.v_p if args.v_p is not None else 10  # Replace with sampling rate of victim task
    
    # AEW length
    anterior_AEW = 1
    posterior_AEW = 3

    # Folder path 
    folder_path = "..\\data\\attack_probability"  
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f'P_{args.file_name}.csv')
    read_folder_path = "..\\data\\schedules"
    read_file_path =  os.path.join(read_folder_path ,f'{args.file_name}')

    with open(file_path, "w") as file:
        print(f'file_name={args.file_name}, path={read_file_path}')
        # with open(f'main\\data\\schedules\\{args.file_name}', 'r') as schedule_file:
        with open(read_file_path, 'r') as schedule_file:
    
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

                # Calculate P for the current sequence
                C = sum(posterior_counter)
                P_C = C / victim_sampling_rate

                # Write P value to the file
                file.write(f"{P_C}\n")

    print(f"Probability values have been saved in {file_path}")

if __name__ == "__main__":
    main()
