import pandas as pd
import matplotlib.pyplot as plt
import glob as glob

'''
View a comparison of learning rate

:author: Matthew Schofield
:version: 2.3.2021
'''
'''
Settings
'''
# Set budget
budgets = [500, 1000, 2000]

# Set metric
metric = "Service Level"

# Result directories
result_directories = {
    "PPO": "../results/DC_0/",
    "TRPO": "../results/trpo/DC_0/",
    "ACKTR": "../results/acktr/DC_0/"
}

# Algorithms compared
rl_algorithms = ["PPO", "TRPO", "ACKTR"]

'''
Execution
'''
# Learning time series storage
learning_time_series = {}

# Step through results
for alg in rl_algorithms:
    # Step through budgets
    for budget in budgets:
        # Budget file name pattern
        name_pattern = "v*steps*" + str(budget) + ".csv"

        # Learning rate files
        step_files = glob.glob(result_directories[alg] + name_pattern)

        # Show step files accumulated
        print("Number of files: " + str(len(step_files)))
        print(step_files)

        # Step through retrieved files
        for i, file in enumerate(step_files):
            # Read in file
            frame = pd.read_csv(file, names=["Reduced Unservice", "Service Level", "Budget"], skiprows=3)

            # Store learning time series
            if not alg in learning_time_series.keys():
                learning_time_series[alg] = frame[metric].values
            else:
                for i, val in enumerate(frame[metric].values):
                    learning_time_series[alg][i] += val

linestyles = ["-.", "--", ":"]
markers = ["s", "^", "o"]
# Plot results
for l, alg in enumerate(rl_algorithms):
    # Data series
    data_series = learning_time_series[alg]/15
    y = []
    for i in range(0, len(data_series)-100, 100):
        y.append(sum(data_series[i:i+100]) / 100)
    plt.plot(range(len(y)), y, label=alg, linestyle=linestyles[l], marker=markers[l], linewidth=5, markersize=18)
plt.xlabel("Episodes (100)", fontsize=32)
plt.yticks([0.92, 0.93, 0.94, 0.95, 0.96, 0.97], labels=[0.92, 0.93, 0.94, 0.95, 0.96, 0.97], fontsize=32)
plt.xticks([0, 20, 40, 60, 80, 100], [0, 20, 40, 60, 80, 100], fontsize=32)
plt.ylabel("Average Service Level per Hour", fontsize=32)
plt.legend(loc="upper left", fontsize=32)
plt.show()
