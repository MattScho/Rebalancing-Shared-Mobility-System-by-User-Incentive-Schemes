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
users_to_id = {
    "5200": [0, 5, 10, 15, 20],
    "5700": [1, 6, 11, 16, 21],
    "6500": [2, 7, 12, 17, 22],
    "7800": [3, 8, 13, 18, 23],
    "10400": [4, 9, 14, 19, 24]
}

users = ["5200", "5700", "6500", "7800", "10400"]

id_to_users = {}

for k in users_to_id.keys():
    for i in users_to_id[k]:
        id_to_users[str(i)] = k
print(id_to_users)

# Initialize data and error recorders
data = {
    "opt": [0, 0, 0, 0, 0],
    "noAgent": [0, 0, 0, 0, 0],
    "v1": [0, 0, 0, 0, 0],
    "v2": [0, 0, 0, 0, 0],
    "v3": [0, 0, 0, 0, 0],
    "v4": [0, 0, 0, 0, 0],
    "v5": [0, 0, 0, 0, 0]
}

# Initialize data and error recorders
acc = {
    "opt": [0, 0, 0, 0, 0],
    "noAgent": [0, 0, 0, 0, 0],
    "v1": [0, 0, 0, 0, 0],
    "v2": [0, 0, 0, 0, 0],
    "v3": [0, 0, 0, 0, 0],
    "v4": [0, 0, 0, 0, 0],
    "v5": [0, 0, 0, 0, 0]
}

errs = {
    "opt": [0, 0, 0, 0, 0],
    "noAgent": [0, 0, 0, 0, 0],
    "v1": [0, 0, 0, 0, 0],
    "v2": [0, 0, 0, 0, 0],
    "v3": [0, 0, 0, 0, 0],
    "v4": [0, 0, 0, 0, 0],
    "v5": [0, 0, 0, 0, 0]
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


    # Set budgets
    budgets = [300, 500, 1000, 2000, 4000, 10000]

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
            # Read in file
            frame = pd.read_csv(file, names=["Reduced Unservice", "Service Level", "Budget"])

            # Get results, using the last 100 indices of the steps
            results = frame[metric].values[-100:]

            # Grab version to make title
            v = file.split("_steps")[-2].split("\\")[-1]
            # Store metric calculations
            data[v][users.index(id_to_users[setting])] += (sum(results) / len(results))
            acc[v][users.index(id_to_users[setting])] += 1


for k in data.keys():
    data[k] = [i/30 for i in data[k]]

plt.ylim([0.75, 1.0])
print(acc)

markers = ["","", "s", "^", "o", "p", "+", "x"]

versionMapper = {
    "opt": "Epr. Optimal",
    "noAgent": "No Agent",
    "v1": "SADUE-A",
    "v2": "S-A",
    "v3": "S-A+",
    "v4": "SAD'-A+",
    "v5": "SA'D'-A+D+"
}
for i, k in enumerate(data.keys()):
    plt.plot(users, data[k], linestyle="--", marker=markers[i], linewidth=5, label=versionMapper[k], markersize=24)
plt.legend(loc="upper right", fontsize=20)
plt.ylabel("Average Service Level per Hour", fontsize=32)
plt.xlabel("Users Per Day", fontsize=32)

# Style plot axis X ticks
plt.xticks(range(len(users)), labels=["5200", "5700 (~+10%)", "6500 (+25%)", "7800 (+50%)", "10400 (+100%)"], fontsize=24)
plt.yticks([0.75, 0.8, 0.85, 0.9, 0.95, 1.0], labels=[0.75, 0.8, 0.85, 0.9, 0.95, 1.0], fontsize=24)
plt.show()

plt.show()