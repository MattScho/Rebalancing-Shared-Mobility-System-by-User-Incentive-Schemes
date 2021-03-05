import pandas as pd
import matplotlib.pyplot as plt
import glob
from statistics import stdev


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

    errs = {
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


            # Store metric calculations
            data[v].append(sum(results) / len(results))

    # Construct plot
    fig, ax = plt.subplots()
    plt.setp(ax, ylim=ylimits)

    print(data)

    # Plot data
    for k in data.keys():
        plt.plot(budgets, data[k], linestyle="--", linewidth=5)
        plt.scatter(budgets, data[k], s=96)
        plt.xscale('log')
        plt.xticks(budgets, budgets, fontsize=24)


    # Set plot labels
    plt.ylabel("Average Service Level per Hour", fontsize=32)
    plt.xlabel("Budget ($ - USD)", fontsize=32)

    plt.show()
