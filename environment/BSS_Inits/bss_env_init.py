'''
Data Structure to define BSS initializations

Schema

stepsPerEpisode = int (24)
systemSize = int (10)
supply = [r1, r2, ..., r100] len 100
users = [
            [ [a1, d1], [a2, d2], ..., [an, dn]],
            [],
            ...,
            []
        ]
description = str, description of the environment
'''
class BSS_Env_Init:

    def __init__(self, stepsPerEpisode, systemSize, supply, users, description):
        # Steps per episode/game, aka number of hours
        self.stepsPerEpisode = stepsPerEpisode

        # Length of one side of the matrix (length of a vector within matrix),
        # the systems are square matrices, therefore systemSize^2 is the total number of elements in the
        # system
        self.systemSize = systemSize

        # Supply of bikes at each region
        self.initSupplies = supply

        # List of users each hour to interact with system
        self.users = users

        # Add a description for init settings
        self.description = description

    def getStepsPerEpisode(self):
        return self.stepsPerEpisode

    def getInitSupply(self):
        return self.initSupplies

    def getUsers(self):
        return self.users

    def getSystemSize(self):
        return self.systemSize

    def getDescription(self):
        return self.description