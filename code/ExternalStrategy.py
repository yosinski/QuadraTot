#! /usr/bin/env python


#from random import choice
#from numpy import array, random, ones, zeros, sin, vstack, hstack, argmax, diag, linalg, dot, exp
#import string, os
#import pickle
#import pdb

from Strategy import Strategy, OneStepStrategy
from util import matInterp
from SineModel import SineModel5



class NEATStrategy(OneStepStrategy):
    '''
    A strategy that calls a NEAT executable to determine a gait
    '''

    def __init__(self, *args, **kwargs):
        super(NEATStrategy, self).__init__(*args, **kwargs)

        self.executable = 'hyperNEAT'
        self.motionFile = 'something.dat'

        self.proc = sp.Popen((self.executable
                              '-a', '-b', 'c',),
                             stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)

    def __del__(self):
        print 'Waiting for %s to exit...' % self.executable
        code = proc.wait()
        print 'Done.'


    def getNext(self):
        '''Get the next point to try.  This reads from the file
        self.motionFile'''

        ff = open(self.motionFile, 'r')
        
        for line in ff:
            nums = [float(xx) for xx in line.split()]
            try:
                positions = vstack((positions, array(nums)))
            except NameError:
                positions = array(nums)
        times = linspace(0,12,positions.shape[0])

        # return function of time
        return lambda time: matInterp(time, times, positions)


    def updateResults(self, dist):
        '''This must be called for the last point that was handed out!

        This communicates back to the running subprocess.
        '''

        dist = float(dist)

        # MAKE SURE TO CALL super().updateResults!
        super(NEATStrategy, self).updateResults(dist)

        # Send fitness to process
        out,err = proc.communicate('%f\n' % dist)

        print 'Got stdout:'
        print out
        print 'Got stderr:'
        print err


    def logHeader(self):
        return '# NEATStrategy starting\n'



def main():
    pass



if __name__ == '__main__':
    main()

