import os
import numpy

def main():
    
    # Lists entered by user
    attacker = [4, 5, 6, 7]  # Replace with attacker task index
    victim = [1]
    victim_sampling_rate = 10  # Replace with sampling rate of victim task

    # AEW length
    anterior_AEW = 1
    posterior_AEW = 3

    #folder path 
    folder_path = "main\\data\\attack_probability"  
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, 'P_FP.csv')

    with open( file_path , "w") as file:

        with open('main\data\schedules\FP_schedule_randomization_idle_time\idle_time_fp_schedules.txt', 'r') as schedule_file:
        #with open('main\data\schedules\MAARS\MAARS_schedules.txt', 'r') as schedule_file:

        
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

    print("Probability values have been saved in /data/attack_probability")

if __name__ == "__main__":
    main()
