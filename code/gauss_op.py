#! /usr/bin/env python

'''
gauss_op.py
@date: 14 October 2010

'''

"""
Employs random hill-climbing with a Gaussian distribution to choose and 
evaluate the parameters of the robots' motion, either by changing one 
parameter completely randomly, or changing one parameter slightly. 
Evaluates each neighbor using user-inputed distance walked.

"""

import math, pdb, sys
import random
from datetime import datetime
from copy import copy
from Robot import Robot
from SineModel import sineModel

def initialState(ranges):
    """ 
    Given the ranges of the different parameters, chooses random values for
    each parameter. The ranges of parameters are in a list of tuples.

    """
    parameters = []  # List of the chosen values for the parameters
    for rang in ranges:
        # Chooses random values for each parameter (initial state)
        if isinstance(rang[0], bool):  # If range is (true, false),
                       # choose true or false
            parameters.append(random.uniform(0,1) > .5)
        else:
            parameters.append(random.uniform(rang[0], rang[1]))
    return parameters

def gauss_neighbor(ranges, parameters):
    """
    Given a list of parameters, picks a random parameter to change, randomly
    changes it based on a Gaussian distribution, and returns a new list.

    """
    ret = copy(parameters)
    index = random.randint(0, len(parameters) - 1)

    if isinstance(ranges[index][0], bool):
        ret[index] = (random.uniform(0,1) > .5)
    else:
        while True:
            changeTo = random.gauss(ret[index], .10 * (ranges[index][1] - 
                                                       ranges[index][0]))
            # Check that randomly generated number is in range
            if ranges[index][0] <= changeTo <= ranges[index][1]:
                ret[index] = changeTo
                break

    return ret

def slightNeighbor(ranges, parameters):
    """
    Given a list of parameters, picks a random parameter to change, and
    decreases or increases it slightly.

    """
    ret = copy(parameters)
    print '  ** Neighbor old', ret
    index = random.randint(0, len(parameters) - 1)

    print ranges
    if isinstance(ranges[index][0], bool):
        ret[index] = (random.uniform(0,1) > .5)
    else:
        if random.randint(0, 1) == 0:  # decrease slightly
            ret[index] = ret[index] - (.1 * (ranges[index][1] - ranges[index][0]))
        else:  # increase slightly
            ret[index] = ret[index] - (.1 * (ranges[index][1] - ranges[index][0]))

    print '  ** Neighbor new', ret
    return ret

def prettyVec(vec):
    return ('[' +
            ' '.join(['%4f' % xx if isinstance(xx,float) else repr(xx) for xx in vec]) +
            ']')
    
def doRun():
    # Parameters are: amp, tau, scaleInOut, flipFB, flipLR
    
    android = Robot(commandRate = 40, loud = False)
    # TODO: motion = Motion()
    # TODO: Move ranges below 
    #ranges = [(0, 400),
    #          (.5, 8),
    #          (-2, 2),
    #          (False, True),
    #          (False, True)]

    ranges = [(0, 400),
              (.5, 8),
              (-2, 2),
              (-1, 1),
              (-1, 1)]

    if len(sys.argv) > 1:
        currentState = [eval(xx) for xx in sys.argv[1].split()]
    else:
        currentState = initialState(ranges)

    statesSoFar = set()  # Keeps track of the states tested so far
    
    bestDistance = -1e100

    stateSoFar = set()

    logFile = open('log.txt', 'a')
    logFile.write('\nOptimize started at %s\n' % datetime.now().ctime())
    logFile.close()
    for ii in range(10000):
        print
        print 'Iteration %2d params' % ii, prettyVec(currentState)

        beginDistance = WiiTrackClient.getPosition()

        # Make sure this state is new, skip otherwise
        if tuple(currentState) in statesSoFar:
            print '*** Skipping duplicate iteration!'
            continue

        stateSoFar.add(tuple(currentState))

        motionModel = lambda time: sineModel(time,
                                             parameters = currentState)

        android.run(motionModel, runSeconds = 10, resetFirst = False,
                    interpBegin = 3, interpEnd = 3)

        endDistance = WiiTrackClient.getPosition()
        
        currentDistance = RunManager.calculateDistance(beginDistance,
                                                       endDistance)

        if currentDistance >= bestDistance:  # Is this a new best?
            bestState = copy(currentState)  # Save new neighbor to best found
            bestDistance = copy(currentDistance)

        print '        best so far', prettyVec(bestState), bestDistance  # Prints best state and distance so far

        # Writes to log file that keeps track of tests so far
        stats = ' '.join([repr(xx) for xx in currentState])
        logFile = open('log.txt', 'a')
        logFile.write(stats + ", " + str(currentDistance) + "\n")
        logFile.close()

        currentState = neighbor(ranges, bestState)

    return bestState  # Return the best solution found (a list of params)

def main():
   doRun()

if __name__ == '__main__':
   main()

