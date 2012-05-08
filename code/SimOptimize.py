import sys, pickle
from SineModel import SineModel5
import simrun
from ExternalStrategy import NEATStrategy
from util import randUniformPoint


def SimOptimize(sim):
    strategy = NEATStrategy(SineModel5.typicalRanges)


    for ii in range(10):
        nextGait = strategy.getNext()

        # Run the gait
        dist = simrun.runSim(nextGait)
        strategy.updateResults(dist)


    print 'NEATStrategy'

    

def main(limit = 10):
    sim = simrun.simrun()
    if limit is None:
        limit = 10000
    
    for ii in xrange(limit):
        SimOptimize(sim)
        sim.getDist()
#        print currentState
        print sim.getDist()

if __name__ == '__main__':
    main()
