#! /usr/bin/env python

'''

@date: 27 October 2010

'''

"""
Different algorithms to find choose and evaluate the parameers of the robot's
motion. Evaluates each neighbor and state using WiiTrackClient.

"""

import sys
from SineModel import SineModel5
from RunManager import RunManager
from Strategy import *



def doRun():
    runman = RunManager()

    # Choose initialState, either from user-inputted parameters or randomly
    if len(sys.argv) > 1:
        currentState = [eval(xx) for xx in sys.argv[1].split()]
    else:
        currentState = runman.initialState(SineModel5.typicalRanges)


    #strategy = UniformStrategy(currentState)
    #strategy = GaussianStrategy(currentState)
    strategy = GradientSampleStrategy(currentState)
    #strategy = LinearRegressionStrategy(currentState)

    #runman.do_many_runs(currentState, lambda state: Neighbor.gaussian(SineModel5.typicalRanges, state))
    #runman.do_many_runs(currentState, lambda state: gradient_search(SineModel5.typicalRanges, state))
    runman.do_many_runs(strategy, SineModel5.typicalRanges)

def main():
    doRun()

if __name__ == '__main__':
    main()
