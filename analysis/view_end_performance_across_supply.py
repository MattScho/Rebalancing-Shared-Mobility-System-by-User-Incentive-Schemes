import pandas as pd
import matplotlib.pyplot as plt
import glob
from statistics import stdev


'''
Process
'''
def bar_plot(ax, data, yerr, colors=None, total_width=0.8, single_width=1, legend=True):
    """
    Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, yerr=yerr[name][x], width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    versionMapper = {
        "noAgent": "No Agent",
        "opt": "Empirically Optimal",
        "v1": "Rep 1",
        "v2": "Rep 2",
        "v3": "Rep 3",
        "v4": "Rep 4",
        "v5": "Rep 5"
    }
    # Draw legend if we need
    if legend:
        ax.legend(bars, [versionMapper[k] for k in data.keys()])

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
    budgets = [300, 500, 1000]

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
            data[v][supplies.index(id_to_supply[setting])] += (sum(results) / len(results))
            acc[v][supplies.index(id_to_supply[setting])] += 1
print("x")
print(data)
for k in data.keys():
    data[k] = [i/15 for i in data[k]]

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
    plt.plot(supplies, data[k], linestyle="--", marker=markers[i], linewidth=5, label=versionMapper[k], markersize=24)
plt.legend(loc="upper right", fontsize=20)
plt.ylabel("Average Service Level per Hour", fontsize=32)
plt.xlabel("Supply", fontsize=32)

# Style plot axis X ticks
plt.xticks(range(len(supplies)), labels=["4500", "4000 (~-10%)", "3375 (-25%)", "2250 (-50%)", "1500 (-66.6%)"], fontsize=24)
plt.yticks([0.75, 0.8, 0.85, 0.9, 0.95, 1.0], labels=[0.75, 0.8, 0.85, 0.9, 0.95, 1.0], fontsize=24)

plt.show()
