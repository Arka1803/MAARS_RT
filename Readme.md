# MULTI-RATE ATTACK AWARE RANDOMIZED SCHEDULING (MAARS)
This codebase is designed to generate multi-rate schedules from task sets produced by the RandfixedSum Algorithm. The generated schedules are then analyzed to calculate two key performance metrics:
1. Inferability Ratio: This metric quantifies the inferability of the generated schedules.
2. Average Attack Probability: This metric computes the average probability of an attack within the generated schedules.

# Requirements

- Python version 3.11
- MATLAB 2022

### Required Packages Installation
```bash
- pip install numpy matplotlib pandas
```
# Usage Overview
The MAARS framework is designed to generate and analyze multi-rate schedules for real-time systems, focusing on inferability ratio and attack probability. The workflow consists of four key steps:

1. __Generate Synthetic Task Sets__ :  Synthetic task sets are created based on user-defined utilization ranges, number of tasks, and hyperperiod length. The script `task_set_generate_randfixedsum.py` performs this.

2. __Generate Multi-Rate Schedules__:  The generated task sets are processed to produce MAARS schedules, which are stored in text files for further analysis. The script `MAARS_multitaskset.py` performs this.

4. __Compute Inferability Ratio (IR)__ : The inferability ratio of the generated schedules is calculated to assess system security, with results stored in CSV format and final plots generated using MATLAB.  The MATLAB scripts `MAARS.m` and `FP_rand` performs this.

3. __Compute Attack Probability (AP)__ : The generated schedules are analyzed to determine the probability of an attack based on specific experimental parameters, with results stored in CSV format and visualized as plots. The script `AP_plot.py --v_i <victim_id> --a_i <attacker_id>` performs this.

The commands to perform these steps are given below in details. Clone the repository:

```bash
git clone https://github.com/Arka1803/MAARS_RT.git
```

## Step 1: Generate Synthetic Task Sets
* To generate synthetic task-sets execute the below script from  `MAARS_RT/main/generate_task_set` directory.
```bash
python3 task_set_generate_randfixedsum.py
```
* This prompts the user to take 3 inputs 
    - Desired utilization range, which the user can give multiple task utilization range with comma separation, e.g. __{0.02-0.18, 0.22-0.38,..}__, 
    - Number of tasks e.g. __{5,10,15,..}__ 
    - Hyperperiod length e.g. __3000__
    
_Note that taking a very high number of tasks with lengthy hyperperiods will take a long time. The plot in both (fig.7 and 8) will be generated for given input in image_

![alt text](pic_input.png)

* Output files are generated inside `/main/data/task_set` directory.


## Step 2: Generate Multi-Rate Schedules

* Run this script from the `/main/rt_schedulers/multi_rate` directory. This process may take a few minutes. 

```bash
python3 MAARS_multitaskset.py
```

_Note that to limit the running time, the no. of schedules has been limited to 100. This can be modified as per requirement._

* The script `MAARS_multitaskset.py` generates schedules of all the task sets at once in the directory `main/data/schedules`. Each schedule text file contains lists having sequences of task IDs representing corresponding task IDs. 

## Step-3: Compute Inferability Ratio (IR) (Reproduce plot for Fig.7)

* The script `IR_parser.py` should be ran with parse arguments inside `/main/inferability_ratio ` such as:

>python3 IR_parser.py [file_name] --v_i <victim_id> --v_p <victim_period> --a_i <attacker_id>

An example has been given below:

```bash
python3 IR_parser.py schedule_util_0.02-0.18_tasks_5.txt --v_i 1 --v_p 12 --a_i 4
```

* Without parse arguments the default `<victim_id>`, `<attacker_id>` and `<victim_period>` is set to 1,4 and 12 respectively.

* The output is a CSV file that is stored in the `main/data/inferability_ratio `with the name `IR_[file_name].csv`, where inferability ratio is plotted in 2nd column against every schedule.

### Plotting Experimental Data (Fig.7)
* Fig.7 plots can be generated by running the matlab files inside `/Plotting/matlab_plot_codes`. 

```bash
matlab -nodisplay -nosplash -r "MAARS; FP_rand;"
```


## Step-4: Compute Attack Probability (AP) (Reproduce plot for Fig.8)

* The attack probabilities are averaged and plotted in Fig.8. To generate AP plot execute `AP_plot.py` from `/main/attack_probability` 


```bash 
python3 AP_plot.py
```

* To generate AP plot with parse arguments, run the script like this:

>`AP_plot.py --v_i <victim_id> --a_i <attacker_id>`.  

Without parse arguments the default `<victim_id>` and `<attacker_id>` is set to 1 and 4 respectively.

* The experimental parameters such as attack-effective windows (AEW), attack and victim task IDs and sampling rate of victim task will be different for each task set. The output is a CSV file that is stored in the `main/data/attack_probability` with the name `P_[file_name].csv.` 

* This script reads the schedule files located at `main/data/schedules/` as its input. The results are exported as a CSV file to the `data/attack_probability` directory and then plots the average of probabilities.


# Publication

The corresponding paper has been accepted at ICCPS in CPS-IOT Week 2025.

MAARS: Multi-Rate Attack-Aware Randomized Scheduling for Securing Real-time Systems, Arkaprava Sain, Sunandan Adhikary, Ipsita Koley, Soumyajit Dey, Dept. of CSE, Indian Institute of Technology Kharagpur, India
