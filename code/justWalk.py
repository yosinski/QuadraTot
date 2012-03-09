#! /usr/bin/env python

'''
Just walks.
'''

import sys
from SineModel import SineModel5
from RunManager import RunManager
from RobotQuadratot import *
from Strategy import *



def main():
    if len(sys.argv) > 2 and sys.argv[1] == '-filt':
        filtFile = sys.argv[2]
        strategy = FileStrategy(filtFile = filtFile)
        motionFunction, logInfo = strategy.getNext()
    elif len(sys.argv) > 2 and sys.argv[1] == '-sine':
        sineModel5Params = [eval(xx) for xx in sys.argv[2].split()]
        print 'Using SineModel5 with params: ', sineModel5Params
        motionFunction = lambda time: SineModel5().model(time,
                                                         parameters = sineModel5Params)
    else:
        #filtFile = 'out/hyperneatTo20gens_101/neat_110115_175446_00014_008_filt'
        filtFile = 'out/hyperneatTo20gens_101/neat_110115_175446_00004_007_filt'
        strategy = FileStrategy(filtFile = filtFile)
        motionFunction, logInfo = strategy.getNext()
    

    
    #runman = RunManager()
    #runman.do_many_runs(strategy, SineModel5.typicalRanges)

    timeScale = .3
    motionFunctionScaled = scaleTime(motionFunction, timeScale)

    robot = RobotQuadratot()
    robot.run(motionFunction, runSeconds = 8, resetFirst = False,
              interpBegin = 2, interpEnd = 2)


if __name__ == '__main__':
    main()
