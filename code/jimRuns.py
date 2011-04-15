#! /usr/bin/env python

import sys
#, pickle
#from SineModel import SineModel5
#from RunManager import RunManager
#from Strategy import *
#from SVMStrategy import SVMLearningStrategy
#from ExternalStrategy import NEATStrategy
#from util import randUniformPoint



def main():
    #neatFile = None
    
    if len(sys.argv) > 1:
        if (len(sys.argv) > 2 and sys.argv[1] == '-SineModel5':
            sineModel5Params = [eval(xx) for xx in sys.argv[2].split()]
            print 'Using SineModel5 with params: ', sineModel5Params
            
            motionFunction = lambda time: SineModel5().model(time,
                                                             parameters = currentState)

            strategy = 
            # Simplex filename
            import pickle
            filename = sys.argv[2]
            ff = open(filename, 'r')
            strategy = pickle.load(ff)
            ff.close()
        elif (len(sys.argv) > 2 and sys.argv[1] == '-neat'):
            neatFile = sys.argv[2]
            currentState = None
        elif (len(sys.argv) > 2 and sys.argv[1] == '-filt'):
            filtFile = sys.argv[2]
            currentState = None
        else:
            # normal
            currentState = [eval(xx) for xx in sys.argv[1].split()]
    else:
        print 'Error: need args'
        sys.exit(1)
        #currentState = randUniformPoint(SineModel5.typicalRanges)

    timeScale = 1
    motionFunctionScaled = scaleTime(motionFunction, timeScale)

    runman = RunManager()
    
    for ii = range(10):
        print 'Iteration', ii
        


    try:
        strategy
    except:
        #strategy = UniformStrategy(currentState, SineModel5.typicalRanges)
        strategy = GaussianStrategy(currentState, SineModel5.typicalRanges)
        #strategy = GradientSampleStrategy(currentState)
        #strategy = LinearRegressionStrategy(currentState)
        #strategy = SimplexStrategy(currentState, SineModel5.typicalRanges)
        #strategy = RandomStrategy(currentState, SineModel5.typicalRanges)
        #strategy = SVMLearningStrategy(currentState, SineModel5.typicalRanges)
        #strategy = NEATStrategy(currentState, SineModel5.typicalRanges, neatFile = neatFile)   # these args aren't used
        #strategy = FileStrategy(filtFile = filtFile)
        
    #runman.do_many_runs(currentState, lambda state: Neighbor.gaussian(SineModel5.typicalRanges, state))
    #runman.do_many_runs(currentState, lambda state: gradient_search(SineModel5.typicalRanges, state))
    runman.do_many_runs(strategy, SineModel5.typicalRanges)



if __name__ == '__main__':
    main()
