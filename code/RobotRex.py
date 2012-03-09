from datetime import datetime
from time import sleep
from types import FunctionType
from copy import copy
from numpy import array

from Motion import lInterp, scaleTime



from RobotQuadratot import *
from ConstantsRex import *


class RobotRex(RobotQuadratot):
    ''''''

    def __init__(self, silentNetFail = False, expectedIds = None, commandRate = 40,
                 loud = False, skipInit = False):
        '''Initialize the robot.
        
        Keyword arguments:

        silentNetworkFail -- Whether or not to fail silently if the
                             network does not find all the dynamixel
                             servos.

        nServos -- How many servos are connected to the robot,
                   i.e. how many to expect to find on the network.

        commandRate -- Rate at which the motors should be commanded,
                   in Hertz.  Default: 40.
        '''

        # WRITE THIS



    def readyPosition(self, persist = False):
        # REWRITE IF DESIRED
        
        if persist:
            self.resetClock()
            while self.time < 2.0:
                self.commandPosition(POS_READY)
                sleep(.1)
                self.updateClock()
        else:
            self.commandPosition(POS_READY)
            sleep(2)

    def commandPosition(self, position, crop = True, cropWarning = False):
        '''Command the given position

        commandPosition will command the robot to move its servos to
        the given position vector.  This vector is cropped to
        the physical limits of the robot and converted to integer

        Positional arguments:
        position -- A length 9 vector of desired positions.

        Keyword arguments:
        cropWarning -- Whether or not to print a warning if the
                       positions are cropped.  Default: False.
        '''

        #DEFINITELY REWRITE
        
        if len(position) != self.nServos:
            raise Exception('Expected postion vector of length %d, got %s instead'
                            % (self.nServos, repr(position)))

        if crop:
            goalPosition = self.cropPosition([int(xx) for xx in position], cropWarning)
        else:
            goalPosition = [int(xx) for xx in position]

        if self.loud:
            posstr = ', '.join(['%4d' % xx for xx in goalPosition])
            print '%.2fs -> %s' % (self.time, posstr)
        
        for ii,actuator in enumerate(self.actuators):
            actuator.goal_position = goalPosition[ii]
        self.net.synchronize()

        #[ac.read_all() for ac in self.actuators]
        #positions = ['%d: %s' % (ii,ac.cache[dynamixel.defs.REGISTER['CurrentPosition']]) for ii,ac in enumerate(self.actuators)]
        #print ' '.join(positions)
        print ''.join(['x' if ac.led else ' ' for ac in self.actuators]) + '  ' ,
        print ' '.join(['%.1f' % ac.current_voltage for ac in self.actuators])

        return goalPosition
    

    def cropPosition(self, position, cropWarning = False):
        '''Crops the given positions to their appropriate min/max values.
        
        Requires a vector of length 9 to be sure the IDs are in the
        assumed order.'''

        # REWRITE IF DESIRED

        if len(position) != self.nServos:
            raise Exception('cropPosition expects a vector of length %d' % self.nServos)

        ret = copy(position)
        for ii in [0, 2, 4, 6]:
            ret[ii]   = max(MIN_INNER, min(MAX_INNER, ret[ii]))
            ret[ii+1] = max(MIN_OUTER, min(MAX_OUTER, ret[ii+1]))
        ret[8] = max(MIN_CENTER, min(MAX_CENTER, ret[8]))

        if cropWarning and ret != position:
            print 'Warning: cropped %s to %s' % (repr(position), repr(ret))
            
        return ret

    def readCurrentPosition(self):
        # REWRITE IF DESIRED

        ret = []
        if len(self.actuators) != self.nServos:
            raise RobotFailure('Lost some servos, now we only have %d' % len(self.actuators))
        for ac in self.actuators:
            #ac.read_all()
            #ret.append(ac.cache[dynamixel.defs.REGISTER['CurrentPosition']])
            ret.append(ac.current_position)
            #sleep(.001)
        return ret

    def pingAll(self):
        # REWRITE IF DESIRED ????? 
        failures = []
        for ii in self.actuatorIds:
            result = self.net.ping(ii)
            if result is False:
                failures.append(ii)
        return failures

