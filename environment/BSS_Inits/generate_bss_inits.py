import numpy as np
from environment.BSS_Inits.bss_env_init import BSS_Env_Init
from environment.BSS_Inits.matrix_creation import MatrixCreator
from environment.BSS_Inits.interest_distributions import InterestDistributions
import pickle as pkl
from glob import glob

'''
Generates .bssEnv files that specify initial

System Size, Steps, Region Supplies and User Demands
'''

def makeSimulationEnvironment(userHourlyActvityDistribution, numberOfUsersPerDay, initialSupplyDistribution,
                              numberOfBikes, description, arrival_distributions, destination_distributions):
    '''
    Here I make a simulation environment

    userHourlyActivityDistribution = [float] - 24, rel percentage of users per hour
    numberOfUsersPerDay = int, number of users per day
    initialSupplyDistribution = [] - 100, rel percentage of supply
    numberOfBikes = int, number of bikes initially distributed
    description = str, text description
    arrival_distributions = [ [float], ...] - 24, hourly arrival distributions
    destination_distributions = [ [float], ...] - 24, hourly destination distributions
    '''

    # 1-day, 24h
    steps = 24

    # 10x10 grid
    systemSize = 10

    # Normalize values to sum to 1.0
    summation_of_user_activity = sum(userHourlyActvityDistribution)
    normalized_user_hourly_distribution = [u/summation_of_user_activity for u in userHourlyActvityDistribution]

    # Use probability distribution to generate users per hour
    # [1,2,...,24], useful for random selection
    element_indices = np.arange(24)

    # Users per hour counts storage
    users_per_hour = np.zeros((24,))

    for u in range(numberOfUsersPerDay):
        # Randomly select using distribution, while it is simple to instead multiply in 3,400
        # This operation is not expensive and adds slight variation to smaller sets
        hour_index = np.random.choice(element_indices, p=normalized_user_hourly_distribution)
        users_per_hour[hour_index] += 1

    # Prepare to create final output
    users_activity_out = []

    # [1,2,..., systemSize], useful for random indexing
    region_indices = np.arange(systemSize ** 2)

    # Step through
    for i, usersInHour in enumerate(users_per_hour):
        # Will store the users for the hour
        hour_activity = []

        # Get the distribution for the hour somewhat vestigial from an early iteration, but
        # the chain of generation and normalization is useful. No need to change for now.
        arrivals_distrib = arrival_distributions[i]
        destinations_distrib = destination_distributions[i]

        # Flatten distribution matrices
        arrivals_distrib = arrivals_distrib.reshape((systemSize ** 2,))
        destinations_distrib = destinations_distrib.reshape((systemSize ** 2,))

        # For number of users in the hour
        for _ in range(int(usersInHour)):
            # Generate arrival and destination interest
            arriv = np.random.choice(region_indices, p=arrivals_distrib)
            dest = np.random.choice(region_indices, p=destinations_distrib)

            # Save User modeled as pair of arrival and destination interest
            hour_activity.append([arriv, dest])

        # Save the hour
        users_activity_out.append(hour_activity)

    # Visual check on number of users per hour

    # Save output of users
    users = np.array(users_activity_out)

    # Supply, create supply distribution
    supply = np.zeros((systemSize**2,))
    for bike in range(numberOfBikes):
        region_index = np.random.choice(region_indices, p=initialSupplyDistribution)
        supply[region_index] += 1

    return BSS_Env_Init(steps, systemSize, supply, users, description)

'''
Generate init environment, or do an analysis
'''
# Construct settings for bss init
title = "s5"
description = "A: inc gauss - gauss; D: gauss - inv gauss; low supply"

# Distribution for probability a user is at a particular hour
userHourlyActivityDistrib = [
    1, .5, .3, .1, .1,
    .5, 2.5, 6, 8.5, 5,
    3.5, 3.5, 4, 4, 4,
    4.5, 5, 9, 10, 9,
    7, 6, 4, 2
]

# Distribution creators
matrix_creator = MatrixCreator()
interest_distributions = InterestDistributions()

destination_distrib_files = glob("generated_user_interests/destinations*")
print(destination_distrib_files)

# Distribution of bike supply
initialSupplyDistribution = matrix_creator.flatten(
    10, matrix_creator.normalizeMatrix(
           10,
           pkl.load(open(destination_distrib_files[17], 'rb'))
        )
   )


arrival_distrib_files = glob("generated_user_interests/arrivals*")
print(arrival_distrib_files)
# Create arrivals and destinations distributions
arrival_distributions = interest_distributions.generate_from_pkls(
    10,
    arrival_distrib_files
)

print(matrix_creator.showDistribution(arrival_distributions[7].reshape(10, 10), "8am Arrivals distribution"))


destination_distributions = interest_distributions.generate_from_pkls(
    10,
    destination_distrib_files
)

counter = 0
# Number of users to simulate in a day
for numberOfBikes in [4500, 4000, 3375, 2250, 1500]:
    # Number of bikes to initially distribute
    for numberOfUsersPerDay in [5200, 5700, 6500, 7800, 10400]:
        print()
        print(counter)
        print("\tbikes: " + str(numberOfBikes))
        print("\tusers: " + str(numberOfUsersPerDay))

        bss_init = makeSimulationEnvironment(userHourlyActivityDistrib, numberOfUsersPerDay, initialSupplyDistribution,
            numberOfBikes, description, arrival_distributions, destination_distributions)

        # Serialize BSS Init object
        pkl.dump(bss_init, open("environment_settings_DC_"+str(counter)+".pkl", 'wb+'))
        counter += 1
