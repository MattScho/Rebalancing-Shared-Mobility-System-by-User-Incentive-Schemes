import pandas as pd
import matplotlib.pyplot as plt
import glob
from statistics import stdev
import numpy as np

'''
Settings
'''
end_perfs = {}

for setting_ in range(25):
    setting = str(setting_)

    # Directory containing results
    results_directory = "../results/DC_"+setting+"/"

    # Metric improvement to visualize and y limit range
    # Either ["Reduced Unservice", "Service Level", "Budget"]
    metric = "Service Level"

    # Vary this to focus on a particular y range, though pyplot's zoom feature could be used
    # If interested in viewing the Budget metric comment out line "plt.setp(axs, ylim=ylimits)"
    ylimits = [0.7, 1.0]


    # Initialize data and error recorders
    data = {
        "opt": [],
        "noAgent": [],
        "v1": [],
        "v2": [],
        "v3": [],
        "v4": [],
        "v5": []
    }

    # Set budgets
    budgets = [300, 500, 1000, 2000, 4000, 10000]

    # Step through budgets
    for budget in budgets:
        # Budget file name pattern
        name_pattern = "*stepsBudget" + str(budget) + ".csv"

        # Learning rate files
        step_files = glob.glob(results_directory + name_pattern)

        # Calculate no agent
        no_op_frame = pd.read_csv(results_directory + "\\noAgent_steps.csv", names=["Reduced Unservice", "Service Level", "Budget"])
        no_op_value = sum(no_op_frame[metric].values[-100:])/100

        # Step through retrieved files
        for i, file in enumerate(step_files):
            print(file)

            # Read in file
            frame = pd.read_csv(file, names=["Reduced Unservice", "Service Level", "Budget"])

            # Get results, using the last 100 indices of the steps
            results = frame[metric].values[-100:]


            # Grab version to make title
            v = file.split("_steps")[-2].split("\\")[-1]
            print(v)


            # Store metric calculations
            data[v].append(((sum(results) / len(results)) - no_op_value) / no_op_value )
            #data[v].append(sum(results) / len(results))

    print(len(data))
    end_perfs[setting_] = data


# Sum budgets
for k in end_perfs.keys():
    for k_r in end_perfs[k].keys():
        print("x")
        print(len(end_perfs[k][k_r]))
        end_perfs[k][k_r] = sum(end_perfs[k][k_r])/6
    accumulation = 0
    for reps in range(1,6):
        accumulation += end_perfs[k]["v"+str(reps)]
    end_perfs[k] = accumulation / 5

output = []
for i in range(25):
    output.append(end_perfs[i])
np_output = np.array(output).reshape((5,5,))
print(np_output)
#plt.imshow(np_output, cmap='Greens')
heatmap = plt.pcolor(np_output, cmap="Greens")
plt.xlim([0,5])
plt.ylim([0,5])
plt.xticks([i+0.5 for i in  range(5)], ["5200", "5700", "6500", "7800", "10400"], fontsize=24)

plt.yticks([i+0.5 for i in  range(5)], ["4500", "4000", "3375", "2250", "1500"], fontsize=24)
cbar = plt.colorbar(heatmap, cmap="Greens")
cbar.ax.tick_params(labelsize=32)
plt.xlabel("Users", fontsize=32)
plt.ylabel("Supply", fontsize=32)
plt.show()