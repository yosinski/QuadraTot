#! /usr/bin/env python

import sys
from SineModel import SineModel5
from RunManager import RunManager
from Motion import scaleTime



USAGE = '''
'''



def usage():
    print USAGE
    sys.exit(1)



def main():
    if len(sys.argv) > 1:
        if len(sys.argv) > 2 and sys.argv[1] == '-SineModel5':
            sineModel5Params = [eval(xx) for xx in sys.argv[2].split()]
            print 'Using SineModel5 with params: ', sineModel5Params
            
            motionFunction = lambda time: SineModel5().model(time,
                                                             parameters = currentState)
        elif len(sys.argv) > 2 and sys.argv[1] == '-neatFiltFile':
            raise Exception('not yet')
            filtFile = sys.argv[2]
            currentState = None
        else:
            usage()
    else:
        usage()

    timeScale = 1
    motionFunctionScaled = scaleTime(motionFunction, timeScale)

    runman = RunManager()
    
    for ii in range(10):
        print
        print 'Iteration', ii
        try:
            runman.run_function_and_log(motionFunctionScaled, 10, 'loggy.txt')
        except:
            print '*** Something failed, skipping'



if __name__ == '__main__':
    main()
