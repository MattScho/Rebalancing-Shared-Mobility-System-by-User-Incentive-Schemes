import pandas as pd
import matplotlib.pyplot as plt
import glob
from statistics import stdev

'''
Process
'''

# Initialize data and error recorders

performance_store = {}

'''
Settings
'''
for setting_ in range(25):
    setting = str(setting_)
    for j, results_directory in enumerate(["../results/DC_"+setting+"/", "../results/trpo/DC_"+setting+"/", "../results/acktr/DC_"+setting+"/"]):

        data = {
            "opt": [0, 0, 0],
            "noAgent": [0, 0, 0],
            "v1": [0, 0, 0],
            "v2": [0, 0, 0],
            "v3": [0, 0, 0],
            "v4": [0, 0, 0],
            "v5": [0, 0, 0]
        }


        # Metric improvement to visualize and y limit range
        # Either ["Reduced Unservice", "Service Level", "Budget"]
        metric = "Service Level"

        # Vary this to focus on a particular y range, though pyplot's zoom feature could be used
        # If interested in viewing the Budget metric comment out line "plt.setp(axs, ylim=ylimits)"
        ylimits = [0.8, 1.0]

            # Set budgets
        budgets = [500, 1000, 2000]

        # Step through budgets
        for budget in budgets:
            # Budget file name pattern
            name_pattern = "*stepsBudget" + str(budget) + ".csv"

            # Learning rate files
            step_files = glob.glob(results_directory + name_pattern)

            # Add no agent and opt files
            step_files.append(results_directory + "\\opt_steps.csv")
            step_files.append(results_directory + "\\noAgent_steps.csv")

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

                data[v][budgets.index(budget)] += (sum(results) / len(results))
        performance_store[setting + " " + str(j)] = data


performance = {
    "ppo": [0, 0, 0],
    "trpo": [0, 0, 0],
    "acktr": [0, 0, 0]
}

agents = ["ppo", "trpo", "acktr"]

for k in performance_store.keys():

    agent_id = int(k.split(" ")[1])
    for i in range(1,6):
        for j in range(3):
            performance[agents[agent_id]][j] += performance_store[k]['v'+str(i)][j]/5
print(performance)

linestyles = ["-.", "--", ":"]
markers = ["s", "^", "o"]

# Plot data
for i, k in enumerate(performance.keys()):
    plt.plot(budgets, performance[k], linestyle=linestyles[i], marker=markers[i], linewidth=5, label=k, markersize=24)
#plt.xscale('log')
plt.xticks(budgets, budgets, fontsize=32)
plt.yticks([0.93, 0.94, 0.95, 0.96, 0.97], labels=[0.93, 0.94, 0.95, 0.96, 0.97], fontsize=32)
plt.legend(loc="upper left", fontsize=32)
# Set plot labels
plt.ylabel("Average Service Level per Hour", fontsize=32)
plt.xlabel("Budget ($ - USD)", fontsize=32)

plt.show()
