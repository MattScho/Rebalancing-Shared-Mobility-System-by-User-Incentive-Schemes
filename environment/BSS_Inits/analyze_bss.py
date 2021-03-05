import numpy as np
from environment.BSS_Inits.bss_env_init import BSS_Env_Init
import matplotlib.pyplot as plt

def showActivityPerHour(bss_init_env):
    '''
    Useful for visualizing total number of users per hours
    '''
    print(bss_init_env.getDescription())

    # Users in init
    init_users = bss_init_env.getUsers()
    system_size_sqr = bss_init_env ** 2

    # Hour counts storage
    perHour = np.zeros((24,))

    # Iterate through hours
    for i in range(24):
        # Init counter for regions
        userArrivals = np.zeros((system_size_sqr,))

        # Count of users per hour
        perHour[i] = len(init_users[i])

        # Count of users per region
        for u in init_users[i]:
            userArrivals[u[0]] += 1

    # Plot users per hour
    plt.bar(x=np.arange(24), height=perHour)
    plt.title("User Arrivals per Hour")
    plt.ylabel("Number of User Arrivals")
    plt.xlabel("Hour [0-23]")
    plt.show()
