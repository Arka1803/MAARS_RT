# MULTI-RATE ATTACK AWARE RANDOMIZED SCHEDULING (MAARS)
This codebase is designed to generate multi-rate schedules from task sets produced by the RandfixedSum Algorithm. The generated schedules are then analyzed to calculate two key performance metrics:
1. Inferability Ratio: This metric quantifies the inferability of the generated schedules.
2. Average Attack Probability: This metric computes the average probability of an attack within the generated schedules.

# Publication

The corresponding paper has been accepted at ICCPS in CPS-IOT Week 2025.

MAARS: Multi-Rate Attack-Aware Randomized Scheduling for Securing Real-time Systems, Arkaprava Sain, Sunandan Adhikary, Ipsita Koley, Soumyajit Dey, Dept. of CSE, Indian Institute of Technology Kharagpur, India


# Requirements

- Python version 3.11

### Required Packages

- `numpy`
- `matplotlib`

# Usage

```bash
# Clone the repository
git clone https://github.com/yourusername/your-repo-name.git
```

The paths in the code are set for windows environment. For using in linux replace them with appropriate path: 




#### Task Set generation
```bash
# Execute the Script inside \main\generate_task_set
python3 task_set_generate_randfixedsum.py
```
Generate task sets based on the given parameters: 
Utilization ranges : 0.2−0.3,0.4−0.5 ,  number of tasks : 15, hyperperiod length : 120. The generated task sets should be saved in the \data\task_set directory. The users can also limit the execution time in the code as per requirement. 


#### Schedule generation
```bash
# Execute the Scripts inside \main\rt_schedulers
python3 [python-file-name].py
```
* Execute the [python-file-name].py to generate the schedules of the task set. The user can copy the task-set data to the code and generate schedules.
* The schedules are generated in the directory \main\data\schedules \[scheduler-directory]\[scheduler-name].txt
```bash
#To generate schedules together run the script 
python3 MAARS_multitaskset.py
````


#### Attack Probability
```bash
# Execute the Script inside \main\attack_prabability
python3 AP_manual.py
```
Takes the \main\data\schedules \[scheduler-directory]\[scheduler-name].txt file as input and outputs CSV file in \data\attack_probability directory. 

```bash
#To generate AP with parse arguments go to \main\attack_probability  
python3 AP_parser.py [file_name] [--v_i V_I] [--v_p V_P] [--a_i A_I]
```

#### Inferability Ratio
```bash
# Execute the Script inside \main\attack_prabability
python3 IR_manual.py
```
Takes the \main\data\schedules \[scheduler-directory]\[scheduler-name].txt file as input and outputs CSV file in \data\inferability_ratio directory. 


```bash
#To generate IR with parse arguments go to \main\inferability_ratio  
python3 IR_parser.py [file_name] [--v_i V_I] [--v_p V_P] [--a_i A_I]
```




````
The user can use these scripts to collect data by changing the task-set parameters (no.of tasks, utilization, hyperperiod etc.) and accordingly generate schedules and anlayse their inferability ratio and attack_probability. 
````

