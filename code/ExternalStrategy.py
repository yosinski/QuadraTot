#! /usr/bin/env python


#from random import choice
#from numpy import array, random, ones, zeros, sin, vstack, hstack, argmax, diag, linalg, dot, exp
#import string, os
#import pickle
#import pdb

from Robot import MIN_INNER, MAX_INNER, MIN_OUTER, MAX_OUTER
from Strategy import Strategy, OneStepStrategy
from util import matInterp
from SineModel import SineModel5



class NEATStrategy(OneStepStrategy):
    '''
    A strategy that calls a NEAT executable to determine a gait
    '''

    def __init__(self, *args, **kwargs):
        super(NEATStrategy, self).__init__(*args, **kwargs)

        self.executable = '/home/team/s/h2_synced/HyperNEAT_v2_5/out/Hypercube_NEAT'
        #self.motionFile = '/home/team/s/h2_synced/HyperNEAT_v2_5/out/spiderJointAngles.txt'
        self.motionFile = 'spiderJointAngles.txt'

        self.proc = sp.Popen((self.executable
                              '-O', 'delme', '-R', '102', '-I', 'SpiderRobotExperiment.dat'),
                             stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)

    def __del__(self):
        print 'Waiting for %s to exit...' % self.executable
        code = self.proc.wait()
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

        # swap and scale positions appropriately
        positions = positions.T[ix_([0,1,4,5,2,3,6,7])].T  # remap to right columns
        # scale from [-1,1] to [0,1]
        positions += 1
        positions *= .5
        # scale from [0,1] to appropriate ranges
        innerIdx = [0, 2, 4, 6]
        outerIdx = [1, 3, 5, 7]
        for ii in innerIdx:
            positions[:,ii] *= (MAX_INNER - MIN_INNER)
            positions[:,ii] += MIN_INNER
        for ii in outerIdx:
            positions[:,ii] *= (MAX_OUTER - MIN_OUTER)
            positions[:,ii] += MIN_OUTER
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
        #out,err = proc.communicate('%f\n' % dist)

        print 'Sending to process: %f' % dist)
        self.proc.stdin.write('%f\n' % dist)

        print 'TRYING READ STDOUT'
        stdout = self.proc.stdout.read()
        print 'TRYING READ STDOUT'
        stderr = self.proc.stderr.read()

        print 'Got stdout:'
        print stdout
        print 'Got stderr:'
        print stderr


    def logHeader(self):
        return '# NEATStrategy starting\n'



def main():
    pass



if __name__ == '__main__':
    main()

