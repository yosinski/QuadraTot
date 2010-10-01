'''

@date: 1 Octoberx 2010

'''

"""
Uses simulated annealing to choose the parameters of the robots' motion.

"""

import math
import random

""" 
Given the ranges of the different parameters, chooses random values for
each parameter. The ranges of parameters are in a list of tuples.

"""
def initialState(ranges):
    parameters = []  # List of the chosen values for the parameters
    for i in ranges:
        # Chooses random values for each parameter (initial state)
        # TODO: Sometimes we need floats and sometimes ints. Hrmm. Need to deal
        parameters.append((random.random() * ranges[i][2]) + ranges[i][1])
    return parameters

"""
Given a list of parameters, picks a random parameter to change, randomly
changes it (TODO: Something more sophisticated), and returns a new list.

"""
def neighbor(ranges, parameters):
    index = random.randint(0, len(parameters) - 1)
    parameters[index] = random.random() * ranges[i][2]) + ranges[i][1])
    return parameters

def annealing():
    ranges = [(0, 2 * math.pi), (0, 360)]  # TODO: Actual ranges are..?
    bestState = initialState(ranges)
    runRobotWith(bestState)  # TODO: Run the robot and return
                                       # the distance it managed to walk
    bestDistance = raw_input("Enter distance walked by Android: ")
    k = 0  # counter
    kmax = 10  # TODO: How many times should we run this? Or ask user to
               # input a negative number when done?

    while k <  kmax:
        newState = neighbor(bestState, ranges)  # Pick some neighbor
        runRobotWith(newState)  # TODO
        newDistance = raw_input("Enter distance walked by Android: ")

        if newDistance > bestDistance:  # Is this a new best?
            bestState = newState  # Save new neightbor to best found
            bestDistance = newDistance

        print bestState, bestDistance  # Prints best state and distance so far
        
        k = k + 1

    return bestState  # Return the best solution found (a list of params)
