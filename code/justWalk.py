#! /usr/bin/env python

'''
Just walks.
'''

import sys
from SineModel import SineModel5
from RunManager import RunManager
from Robot import *
from Strategy import *



def main():
    if len(sys.argv) > 1:
        filtFile = sys.argv[1]
    else:
        filtFile = 'out/hyperneatTo20gens_101/neat_110115_175446_00014_008_filt'


    
    strategy = FileStrategy(filtFile = filtFile)
    #runman = RunManager()
    #runman.do_many_runs(strategy, SineModel5.typicalRanges)

    motionFunction, logInfo = strategy.getNext()

    robot = Robot()
    robot.run(motionFunction, runSeconds = 8, resetFirst = False,
              interpBegin = 2, interpEnd = 2)


if __name__ == '__main__':
    main()
