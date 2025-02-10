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

1. __Generate Synthetic Task Sets__ :  Using the RandfixedSum algorithm, synthetic task sets are created based on user-defined utilization ranges, number of tasks, and hyperperiod length. 

2. __Generate Multi-Rate Schedules__:  The generated task sets are processed to produce MAARS schedules, which are stored in text files for further analysis.

3. __Compute Attack Probability (AP)__ : The generated schedules are analyzed to determine the probability of an attack based on specific experimental parameters, with results stored in CSV format and visualized as plots.

4. __Compute Inferability Ratio (IR)__ : The inferability ratio of the generated schedules is calculated to assess system security, with results stored in CSV format and final plots generated using MATLAB.

The commands to perform these steps are given below:


## Step 1: Task Set generation
* To generate synthetic task-sets execute the below script from  `MAARS_RT` directory.
```bash
cd main/generate_task_set
python3 task_set_generate_randfixedsum.py
```
* This prompts the user to take 3 inputs 
    - Desired utilization range, which the user can give multiple task utilization range with comma separation, e.g. __{0.02-0.18, 0.22-0.38,..}__, 
    - Number of tasks e.g. __{5,10,15,..}__ 
    - Hyperperiod length e.g. __3000__
    
_Note that taking a very high number of tasks with lengthy hyperperiods will take a long time. The plot in both (fig.7 and 8) will be generated for given input in image_

![alt text](pic_input.png)

## Step 2: Schedule generation

* the script `MAARS_multitaskset.py` generates schedules of all the task sets at once in the directory `main/data/schedules`. This process may take a few minutes. Run this script from the `/main/attack_probability directory`.

```bash
cd ../rt_schedulers/multi-rate
python3 MAARS_multitaskset.py
```
* Each schedule text file contains lists having sequences of task IDs representing corresponding task IDs. 
 
_Note that to limit the running time, the no. of schedules has been limited to 100. This can be modified as per requirement._

## Step-3: Collect and Plot Attack Probability Data (Produce data for Fig.8)
* The attack probabilities are averaged and plotted in Fig.8. To generate AP plot execute `AP_plot.py` from `/main/attack_probability` 

```bash
cd ../../attack_probability  
python3 AP_plot.py --v_i 1 --a_i 4
```
* The experimental parameters such as attack-effective windows (AEW), attack and victim task IDs and sampling rate of victim task will be different for each task set. The output is a CSV file that is stored in the `main/data/attack_probability` with the name `P_[file_name].csv.` 

* Takes the schedule file located at main/data/schedules/ as its input. The results are exported as a CSV file to the data/attack_probability directory.

## Step-4: Collect and Plot Inferability Ratio Data (for Fig.7)

* The script `IR_parser.py` should be ran with parse arguments inside `\main\inferability_ratio `.


```bash
cd ../inferability_ratio
python3 IR_parser.py schedule_util_0.02-0.18_tasks_5.txt --v_i 1 --v_p 20 --a_i 4
```
* The experimental parameters such as attack-effective windows (AEW), attack and victim task IDs and sampling rate of victim task will be different for each task set.

* The output is a CSV file that is stored in the `main/data/inferability_ratio `with the name `IR_[file_name].csv`

Plotting Experimental Data (Fig.7)

* Fig.7 plots can be generated by running the maylab files inside `/Plotting/matlab_plot_codes`. 

```bash
cd ../../Plotting/matlab_plot_codes
matlab -nodisplay -r "MAARS,FP_rand; exit"
```
# Publication

The corresponding paper has been accepted at ICCPS in CPS-IOT Week 2025.

MAARS: Multi-Rate Attack-Aware Randomized Scheduling for Securing Real-time Systems, Arkaprava Sain, Sunandan Adhikary, Ipsita Koley, Soumyajit Dey, Dept. of CSE, Indian Institute of Technology Kharagpur, India
