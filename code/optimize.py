#! /usr/bin/env python

'''

@date: 1 Octoberx 2010

'''

"""
Uses random movements and manual optimization to choose the parameters
of the robots' motion.

"""

import math, pdb
import random
from copy import copy
from Robot import runRobotWith, cropPositions
from SineModel import sineModel

""" 
Given the ranges of the different parameters, chooses random values for
each parameter. The ranges of parameters are in a list of tuples.

"""
def initialState(ranges):
    parameters = []  # List of the chosen values for the parameters
    for rang in ranges:
        # Chooses random values for each parameter (initial state)
        # TODO: Sometimes we need floats and sometimes ints. Hrmm. Need to deal
        if isinstance(rang[0], bool):
            parameters.append(random.uniform(0,1) > .5)
        else:
            parameters.append(random.uniform(rang[0], rang[1]))
    return parameters

"""
Given a list of parameters, picks a random parameter to change, randomly
changes it (TODO: Something more sophisticated), and returns a new list.

"""
def neighbor(ranges, parameters):
    ret = copy(parameters)
    print '  ** Neighbor old', ret
    index = random.randint(0, len(parameters) - 1)

    print ranges
    if isinstance(ranges[index][0], bool):
        ret[index] = (random.uniform(0,1) > .5)
    else:
        ret[index] = random.uniform(ranges[index][0], ranges[index][1])

    print '  ** Neighbor new', ret
    return ret



def doRun():
    # Parameters are:     amp, tau, scaleInOut, flipFB, flipLR

    ranges = [(0, 400),
              (.5, 8),
              (-2, 2),
              (False, True),
              (False, True)]

    ranges = [(0, 400),
              (.5, 8),
              (-2, 2),
              (-1, 1),
              (-1, 1)]
    currentState = initialState(ranges)

    #runRobotWith(bestState)  # TODO: Run the robot and return
    #                                   # the distance it managed to walk
    #bestDistance = raw_input("Enter distance walked by Android: ")
    bestDistance = -1e100

    #k = 0  # counter
    #kmax = 10  # TODO: How many times should we run this? Or ask user to
    #           # input a negative number when done?

    for ii in range(10000):
        print
        print 'Iteration', ii, 'params', currentState
        
        motionModel = lambda time: sineModel(time,
                                             parameters = currentState,
                                             croppingFunction = cropPositions)

        runRobotWith(motionModel)

        currentDistance = float(raw_input("Enter distance walked by Android: "))

        if currentDistance >= bestDistance:  # Is this a new best?
            bestState = copy(currentState)  # Save new neightbor to best found
            bestDistance = copy(currentDistance)

        print "best so far", bestState, bestDistance  # Prints best state and distance so far

        currentState = neighbor(ranges, bestState)  # Pick some neighbor


    return bestState  # Return the best solution found (a list of params)



def main():
    doRun()



if __name__ == '__main__':
    main()
