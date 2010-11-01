#! /usr/bin/env python

'''

@date: 27 October 2010

'''

"""
Different algorithms to find choose and evaluate the parameers of the robot's
motion. Evaluates each neighbor and state using WiiTrackClient.

"""

import math, pdb, sys
import random
from datetime import datetime
from copy import copy
from Robot import Robot
from SineModel import SineModel5
from RunManager import RunManager
from Neighbor import Neighbor

def gradient_search(ranges, currentState): 
    """
    N-dimensional policy gradient algorithm. During each iteration of the main
    loop we sample t policies near currentState to estimate the gradient
    around currentState, then move currentState by an amount of eta in the
    most favorable direction. Adapted from Nate Kohl and Peter Stone,
    UT Ausin/ICRA 2004.
    
    """
    # Generate random policies near currentState
    random_policies = []
    
    epsilon = .05
    # Evaluate t=8 policies per iteration
    for i in range(8):
        random_policies.append(Neighbor.gradient(ranges, currentState, epsilon))

    runman = RunManager()
    
    # Evaluate each random policy.
    for neighbor in random_policies:
        neighbor.append(runman.run_robot(neighbor))
        print '        Random policy %2d params' % random_policies.index(neighbor), runman.prettyVec(neighbor)
    
    # Average the scores for all random policies
    adjustment = []  # Adjustment vector
    for n in range(len(ranges)):
         # Keep track of number of policies with pos/neg/0 perturbation
         # in dimension n
        num_epos = num_eneg = num_zero = 0
        avg_epos = avg_eneg = avg_zero = 0
        for neighbor in random_policies:
            if neighbor[n] > currentState[n]:  # positive perturbation
                avg_epos = avg_epos + neighbor[len(neighbor) - 1]
                num_epos = num_epos + 1
            if neighbor[n] < currentState[n]:  # negative perturbation
                avg_eneg = avg_eneg + neighbor[len(neighbor) - 1]
                num_eneg = num_eneg + 1
            if neighbor[n] == currentState[n]:  # zero perturbation
                avg_zero = avg_zero + neighbor[len(neighbor) - 1]
                num_zero = num_zero + 1
        
        # Finish calculating averages.        
        try:
            avg_epos = avg_epos / num_epos
        except ZeroDivisionError:
            avg_epos = 0
        
        try: 
            avg_eneg = avg_eneg / num_eneg
        except ZeroDivisionError:
            avg_eneg = 0
            
        try:
            avg_zero = avg_zero / num_zero
        except ZeroDivisionError:
            avg_zero = 0
        
        if avg_zero > avg_epos and avg_zero > avg_eneg:
            adjustment.append(0)
        else:
            adjustment.append(avg_epos - avg_eneg)
    
    # Calculate adjustment vector for each dimension, multiplying with a
    # scalar step-size eta, so that our adjustment will remain a fixed
    # size each iteration
    eta = .1
    for param in adjustment:
        if param < 0:
            param = - (eta * (ranges[n][1] - ranges[n][0]))
        if param > 0:
            param = eta * (ranges[n][1] - ranges[n][0])
        else:
            param = 0
    nextState = [currentState, adjustment]
    return [sum(value) for value in zip(*nextState)]

def doRun():
    runman = RunManager()

    # Choose initialState, either from user-inputted parameters or randomly
    if len(sys.argv) > 1:
        currentState = [eval(xx) for xx in sys.argv[1].split()]
    else:
        currentState = runman.initialState(SineModel5.typicalRanges)

    runman.do_many_runs(currentState, lambda state: Neighbor.gaussian(SineModel5.typicalRanges, state))
    #runman.do_many_runs(currentState, lambda state: gradient_search(SineModel5.typicalRanges, state))

def main():
    doRun()

if __name__ == '__main__':
    main()
