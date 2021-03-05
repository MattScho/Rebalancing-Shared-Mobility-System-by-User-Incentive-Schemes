import pandas as pd
import matplotlib.pyplot as plt
import glob
from statistics import stdev


'''
Process
'''

'''
Settings
'''
# Map of supplies to environment id
supply_to_id = {
    "4500": [0, 1, 2, 3, 4],
    "4000": [5, 6, 7, 8, 9],
    "3375": [10, 11, 12, 13, 14],
    "2250": [15, 16, 17, 18, 19],
    "1500": [20, 21, 22, 23, 24]
}

supplies = ["4500", "4000", "3375", "2250", "1500"]

id_to_supply = {}

for k in supply_to_id.keys():
    for i in supply_to_id[k]:
        id_to_supply[str(i)] = k
print(id_to_supply)

# Initialize data and error recorders
data = {
    "300": [0, 0, 0, 0, 0],
    "500": [0, 0, 0, 0, 0],
    "1000": [0, 0, 0, 0, 0],
    "2000": [0, 0, 0, 0, 0],
    "4000": [0, 0, 0, 0, 0],
    "10000": [0, 0, 0, 0, 0]

}
acc = {
    "300": [0, 0, 0, 0, 0],
    "500": [0, 0, 0, 0, 0],
    "1000": [0, 0, 0, 0, 0],
    "2000": [0, 0, 0, 0, 0],
    "4000": [0, 0, 0, 0, 0],
    "10000": [0, 0, 0, 0, 0]

}
'''
Settings
'''
for setting_ in range(25):
    setting = str(setting_)

    # Directory containing results
    results_directory = "../results/DC_"+setting+"/"

    # Metric improvement to visualize and y limit range
    # Either ["Reduced Unservice", "Service Level", "Budget"]
    metric = "Service Level"

    # Vary this to focus on a particular y range, though pyplot's zoom feature could be used
    # If interested in viewing the Budget metric comment out line "plt.setp(axs, ylim=ylimits)"
    ylimits = [0.65, 1.0]

    # Set budgets
    budgets = [300, 500, 1000, 2000, 4000, 10000]

    # Step through budgets
    for budget in budgets:
        # Budget file name pattern
        name_pattern = "*stepsBudget" + str(budget) + ".csv"

        # Learning rate files
        step_files = glob.glob(results_directory + name_pattern)

        # Add no agent and opt files

        # Step through retrieved files
        for i, file in enumerate(step_files):
            # Read in file
            frame = pd.read_csv(file, names=["Reduced Unservice", "Service Level", "Budget"])

            # Get results, using the last 100 indices of the steps
            results = frame[metric].values[-100:]

            # Grab version to make title
            print(file)
            v = file.split("Budget")[1].split("\\")[-1].split(".")[0]
            data[v][supplies.index(id_to_supply[setting])] += (sum(results) / len(results))
            acc[v][supplies.index(id_to_supply[setting])] += 1

for k in data.keys():
    data[k] = [i/25 for i in data[k]]



plt.ylim([0.65, 1.0])

data_out = []

for k in data.keys():
    data_out.append(data[k])

markers = ["s", "^", "o", "p", "+", "x"]

print(data_out)
for l, data in enumerate(data_out):
    plt.plot(supplies, data, linestyle="--", marker=markers[l], linewidth=5, label=budgets[l], markersize=24)

plt.legend(loc="upper right", fontsize=20)

plt.ylabel("Service Level", fontsize=32)
plt.xlabel("Supply", fontsize=32)

# Style plot axis X ticks
plt.xticks(range(len(supplies)), labels=["4500", "4000 (~-10%)", "3375 (-25%)", "2250 (-50%)", "1500 (-66.6%)"], fontsize=24)
plt.yticks([0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], labels=[0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], fontsize=24)
plt.show()
