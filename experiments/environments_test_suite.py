import sys

# Important for cloud compute
# Change this to the directory that contains the environments directory
sys.path.insert(0, "/home/")

# Imports
from environment.bss_controller_rep_1 import BSS_Controller_Rep1
from environment.bss_controller_rep_2 import BSS_Controller_Rep2
from environment.bss_controller_rep_3 import BSS_Controller_Rep3
from environment.bss_controller_rep_4 import BSS_Controller_Rep4
from environment.bss_controller_rep_5 import BSS_Controller_Rep5
import numpy as np
from stable_baselines import PPO2
from stable_baselines.common.policies import MlpPolicy
import time
import pickle as pkl

'''
Experimental Set-Up
'''
for i in range(25):
    bss_init_env = "DC_" + str(i)
    env_settings_init = pkl.load(open("../environment/generated_environments/environment_settings_" + bss_init_env + ".pkl", 'rb'))
    accumulatedRew = 0
    iterations = 0
    learnSteps = 500000
    evaluationLen = 2400
    for budget in [300, 500, 1000, 2000, 4000, 10000]:
        for env, expName in [
            (
                BSS_Controller_Rep1(env_settings_init, budget, open(bss_init_env + "/v1_stepsBudget" + str(budget) + ".csv", 'a+')),
                "rep1"
            ),
            (
                BSS_Controller_Rep2(env_settings_init, budget, open(bss_init_env + "/v2_stepsBudget" + str(budget) + ".csv", 'a+')),
                "rep2"
            ),
            (
                BSS_Controller_Rep3(env_settings_init, budget, open(bss_init_env + "/v3_stepsBudget" + str(budget) + ".csv", 'a+')),
                "rep3"
            ),
            (
                BSS_Controller_Rep4(env_settings_init, budget, open(bss_init_env + "/v4_stepsBudget" + str(budget) + ".csv", 'a+')),
                "rep4"
            ),
            (
                BSS_Controller_Rep5(env_settings_init, budget, open(bss_init_env + "/v5_stepsBudget" + str(budget) + ".csv", 'a+')),
                "rep5"
        )]:

            accumulatedRew = 0
            iterations = 0
            outFile = open(bss_init_env + "/" + expName + "_perfBudget" + str(budget) + ".csv", 'a+')
            agent = PPO2(MlpPolicy, env)
            state = env.reset()
            start = time.time()
            print("Beginning to learn " + expName)
            agent.learn(learnSteps)
            print(time.time() - start)
            print("\tDone Learning")
            for _ in range(evaluationLen):
                action = agent.predict(state)
                state, reward, done, info = env.step(action[0])
                accumulatedRew += reward
                iterations += 1
                if done:
                    outFile.write(str("%.4f" % (accumulatedRew/iterations)) + "," + str(env.getBudget()) + "\n")
                    accumulatedRew = 0
                    iterations = 0
                    env.reset()
            outFile.close()
            env.close()

    '''
    No Agent
    '''
    print("No agent")
    budget = 0
    env = BSS_Controller_Rep1(env_settings_init, budget, open(bss_init_env + "/noAgent_steps.csv", 'a+'))
    env.reset()
    noAgent = open("noAgent.csv", "a+")
    env.reset()
    for _ in range(evaluationLen):
        state, reward, done, info = env.step(np.zeros((100,))) # take a random action

        accumulatedRew += reward
        iterations += 1
        if done:
            noAgent.write(str("%.4f" % (accumulatedRew/iterations)) + "," + str(env.getBudget()) + "\n")
            accumulatedRew = 0
            iterations = 0
            env.reset()
    noAgent.close()
    env.close()


    '''
    EmpOpt Agent
    '''
    print("Opt agent")
    accumulatedRew = 0
    iterations = 0
    env = BSS_Controller_Rep1(env_settings_init, 99999999, open(bss_init_env+"/opt_steps.csv", 'a+'))
    env.reset()
    noAgent = open(bss_init_env + "/opt.csv", "a+")
    env.reset()
    for _ in range(evaluationLen):
        state, reward, done, info = env.step(np.full((100,), 4.0))

        accumulatedRew += reward
        iterations += 1
        if done:
            noAgent.write(str("%.4f" % (accumulatedRew/iterations)) + "," + str(env.getBudget()) + "\n")
            accumulatedRew = 0
            iterations = 0
            env.reset()
    noAgent.close()
    env.close()
