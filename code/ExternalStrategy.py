#! /usr/bin/env python


from numpy import array, ix_, vstack, linspace, hstack, ones
from time import sleep
import os

from Robot import MIN_INNER, MAX_INNER, MIN_OUTER, MAX_OUTER, NORM_CENTER
from Strategy import Strategy, OneStepStrategy
from util import matInterp
from SineModel import SineModel5
import subprocess as sp
from asyncproc import Process


class NEATStrategy(OneStepStrategy):
    '''
    A strategy that calls a NEAT executable to determine a gait
    '''

    def __init__(self, *args, **kwargs):
        super(NEATStrategy, self).__init__(*args, **kwargs)

        self.executable = '/home/team/s/h2_synced/HyperNEAT_v2_5/out/Hypercube_NEAT'
        #self.motionFile = '/home/team/s/h2_synced/HyperNEAT_v2_5/out/spiderJointAngles.txt'
        self.motionFile = 'spiderJointAngles.txt'
        self.datFile    = '/home/team/s/h2_synced/HyperNEAT_v2_5/out/SpiderRobotExperiment.dat'

        #self.proc = sp.Popen((self.executable,
        #                      '-O', 'delme', '-R', '102', '-I', self.datFile),
        #                     stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
        #os.system('%s -O delme -R 102 -I %s' % (self.executable, self.datFile))
        neatFile = kwargs.get('neatFile', None)
        if neatFile is None:
            self.proc = Process((self.executable,
                                 '-O', 'delme', '-R', '102', '-I',
                                 self.datFile))
        else:
            self.proc = Process((self.executable,
                                 '-O', 'delme', '-R', '102', '-I',
                                 self.datFile, '-X', neatFile, '-XG', '1'))
            
        #'%s -O delme -R 102 -I %s' % (self.executable, self.datFile))


    def __del__(self):
        print 'Waiting for %s to exit...' % self.executable,
        code = self.proc.wait()
        print 'done.'


    def getNext(self):
        '''Get the next point to try.  This reads from the file
        self.motionFile'''

        #print 'TRYING READ STDOUT'
        #stdout = self.proc.stdout.read()
        #print 'TRYING READ STDERR'
        #stderr = self.proc.stderr.read()

        #print 'STDOUT:'
        #print stdout
        #print 'STDERR:'
        #print stderr

        while True:

            out = self.proc.read()
            if out != '':
                print 'Got stdout:'
                print out
            out = self.proc.readerr()
            if out != '':
                print 'Got stderr:'
                print out

            try:
                ff = open(self.motionFile, 'r')
            except IOError:
                print 'File does not exist yet'
                sleep(.2)
                continue

            lines = ff.readlines()
            nLines = len(lines)
            if nLines < 480:
                print 'Oops, only %d lines!' % nLines
                ff.close()
                sleep(.2)
                continue
            break

        for ii,line in enumerate(lines):
            #print 'line', ii, 'is', line
            nums = [float(xx) for xx in line.split()]
            if ii == 0:
                positions = array(nums)
            else:
                positions = vstack((positions, array(nums)))

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
        # append a column of 512s
        positions = hstack((positions,
                            NORM_CENTER * ones((positions.shape[0],1))))
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

        print 'Sending to process: %f' % dist
        self.proc.write('%f\n' % dist)

        #print 'TRYING READ STDOUT'
        #stdout = self.proc.stdout.read()
        #print 'TRYING READ STDOUT'
        #stderr = self.proc.stderr.read()
        #
        #print 'Got stdout:'
        #print stdout
        #print 'Got stderr:'
        #print stderr

        out = self.proc.read()
        if out != '':
            print 'Got stdout:'
            print out
        out = self.proc.readerr()
        if out != '':
            print 'Got stderr:'
            print out

    def logHeader(self):
        return '# NEATStrategy starting\n'



def main():
    pass



if __name__ == '__main__':
    main()

