"""
v2

Reduced state space to supply and RB

author Matthew Schofield
version 11.28.2020
"""
from gym import spaces
import numpy as np
from environment.bss_controller_rep_1 import BSS_Controller_Rep1

class BSS_Controller_Rep2(BSS_Controller_Rep1):
    '''
    Author Matthew Schofield
    Version 11.16.2020

    Changes from paper:

    Reduced state space to only supply
    '''

    def __init__(self, systemInitObj, budget, stepFile):
        """
        Initializes the environment
        """
        super().__init__(systemInitObj, budget, stepFile)
        self.observation_space = spaces.Box(0.0, 100.0, shape=(self.systemSize**2,), dtype=np.float32)

    '''
    Helper methods
    '''
    def buildState(self):
        state = self.S
        return state

