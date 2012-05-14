import sys, pickle, pdb
from SineModel import SineModel5
from simrun import simrun
from ExternalStrategy import NEATStrategy
from util import randUniformPoint


def SimOptimize():
    strategy = NEATStrategy(SineModel5.typicalRanges)
    print 'NEATStrategy'
    sim = simrun()
    trial = 0
    for ii in range(10000):
        nextGait = strategy.getNext()
        # Run the gait
        dist = sim.runSim(nextGait)
        strategy.updateResults(dist)
        trial += 1
        print 'Trial', trial, 'moved', dist
        print

def main(limit = 10):
#    sim = simrun.simrun()
 #   if limit is None:
  #      limit = 10000
   # 
   # for ii in xrange(limit):
    #    SimOptimize(sim)
     #   sim.getDist()
#        print currentState
      #  print sim.getDist()
      SimOptimize()

if __name__ == '__main__':
    main()
