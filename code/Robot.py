import os, dynamixel, time, datetime
from RobotParams import *
from Motion import lInterp

'''
Much inspiration taken from http://code.google.com/p/pydynamixel/
'''



'''Min and max values for the QuadraTot robot, based on some tests.

Note that these values will avoid collisions only for each servo
individually.  More complex collisions are still possible given
certain vectors of motor position.
'''

MIN_INNER = 150
MAX_INNER = 770
MIN_OUTER = 30
MAX_OUTER = 940
MIN_CENTER = 512 - 180
MAX_CENTER = 512 + 180

POS_FLAT      = [512] * 9
POS_READY     = [800,  40] * 4 + [512]
POS_HALFSTAND = [700, 100] * 4 + [512]
POS_STAND     = [512, 150] * 4 + [512]



class Robot():
    ''''''

    def __init__(self, silentNetFail = False, nServos = 9):
        '''Initialize the robot.
        
        Keyword arguments:

        silentNetworkFail -- Whether or not to fail silently if the
                             network does not find all the dynamixel
                             servos.

        nServos -- How many servos are connected to the robot,
                   i.e. how many to expect to find on the network.
        '''

        # The number of Dynamixels on our bus.
        self.nServos = nServos

        if self.nServos != 9:
            raise Exception('Unfortunately, the Robot class currently assumes 9 servos.')

        # Set your serial port accordingly.
        if os.name == "posix":
            portName = "/dev/ttyUSB0"
        else:
            portName = "COM11"

        # Default baud rate of the USB2Dynamixel device.
        self.baudRate = 1000000

        serial = dynamixel.SerialStream(port=portName, baudrate=baudRate, timeout=1)
        self.net = dynamixel.DynamixelNetwork(serial)

        print "Scanning for Dynamixels...",
        self.net.scan(0, self.nServos-1)

        self.actuators = list()

        for dyn in net.get_dynamixels():
            print dyn.id,
            self.actuators.append(net[dyn.id])
        print "...Done"

        if len(self.actuators) != self.nServos and not silentNetFail:
            raise Exception('Expected to find %d servos on network, but only got %d (%s)'
                            % (self.nServos, len(self.actuators), repr(self.actuators)))


    def run(self, motionFunction, runSeconds = 10, resetFirst = True
            interpBegin = 0, interpEnd = 0):
        '''Run the robot with a given motion generating function.

        Positional arguments:
        
        motionFunction -- Function used to generate the desired motor
                          positions.  This function must take a single
                          argument -- time, in seconds -- and must
                          return the desired length 9 vector of motor
                          positions.  The current implementation
                          expects that this function will be
                          deterministic.
        
        Keyword arguments:

        runSeconds -- How many seconds to run for.  This is in
                      addition to the time added for interpBegin and
                      interpEnd, if any.  Default: 10

        resetFirst -- Begin each run by resetting the robot to its
                      base position, currently implemented as a
                      transition from CURRENT -> POS_FLAT ->
                      POS_READY.  Default: True

        interpBegin -- Number of seconds over which to interpolate
                      from current position to commanded positions.
                      If this is not None, the robot will spend the
                      first interpBegin seconds interpolating from its
                      current position to that specified by
                      motionFunction.  This should probably be used
                      for motion models which do not return POS_READY
                      at time 0.  Default: None

        interpEnd -- Same as interpBegin, but at the end of motion.
                      If interpEnd is not None, interpolation is
                      performed from final commanded position to
                      POS_READY, over the given number of seconds.
                      Default: None
        '''

        #net, actuators = initialize()

        #def run(self, motionFunction, runSeconds = 10, resetFirst = True
        #    interpBegin = 0, interpEnd = 0):

        for actuator in self.actuators:
            actuator.moving_speed = 90
            actuator.synchronized = True
            actuator.torque_enable = True
            actuator.torque_limit = 1000
            actuator.max_torque = 1000

        print 'Starting motion.'

        time0 = datetime.datetime.now()
        startingPos = None

        if resetFirst:
            while True:
                if startingPos == None:
                    startingPos = currentPositions(actuators)
                timeDiff = datetime.datetime.now() - time0
                seconds  = timeDiff.seconds + timeDiff.microseconds/1e6

                if seconds < 3:
                    goal = lInterp(seconds, [0, 3], startingPos, POS_FLAT)
                

        while True:
            if startingPos == None:
                startingPos = currentPositions(actuators)
            timeDiff = datetime.datetime.now() - time0
            seconds  = timeDiff.seconds + timeDiff.microseconds/1e6

            if seconds < 3:
                goal = lInterp(seconds, [0, 3], startingPos, POS_FLAT)
            elif seconds < 6:
                goal = lInterp(seconds, [3, 6], POS_FLAT, POS_READY)
            #elif seconds < 10:
            #    goal = lInterp(seconds, [6, 10], POS_READY, POS_HALFSTAND)
            elif seconds < runSeconds + 6:
                goal = paramFunction(seconds - 6)
            else:
                break

            #print 'At %3.3f, commanding:' % seconds,

            self.commandPosition(........)
            #print

            #for actuator in actuators[:8]:
            #    actuator.read_all()
            #    time.sleep(0.01)
            #for actuator in actuators[:8]:
            #    print actuator.cache[dynamixel.defs.REGISTER['Id']], actuator.cache[dynamixel.defs.REGISTER['CurrentPosition']]
            time.sleep(.025)

    def commandPosition(self, position, cropWarning = False):
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

        goalPosition = self.cropPosition(position, cropWarning)
        
        for ii,actuator in enumerate(self.actuators):
            gg = int(round(goal[ii],0))
            #gg = max(min(gg, servoMax), servoMin)
            actuator.goal_position = gg
            #print gg,
        net.synchronize()
        



    def cropPosition(position, cropWarning = False):
        '''Crops the given positions to their appropriate min/max values.
        
        Requires a vector of length 9 to be sure the IDs are in the
        assumed order.'''

        if len(pos) != self.nServos:
            raise Exception('cropPositions expects a vector of length %d' % self.nServos)

        ret = copy(position)
        for ii in [0, 2, 4, 6]:
            ret[ii]   = max(MIN_INNER, min(MAX_INNER, ret[ii]))
            ret[ii+1] = max(MIN_OUTER, min(MAX_OUTER, ret[ii+1]))
        ret[8] = max(MIN_CENTER, min(MAX_CENTER, ret[8]))

        if cropWarning and ret != position:
            print 'Warning: cropped %s to %s' % (repr(position), repr(ret))
            
        return ret


    def currentPositions(actuators):
        ret = []
        for ac in actuators:
            ac.read_all()
            ret.append(ac.cache[dynamixel.defs.REGISTER['CurrentPosition']])
        return ret



    def printStatus(actuators):
        pos = currentPositions(actuators)
        print 'Positions:', ' '.join(['%d:%d' % (ii,pp) for ii,pp in enumerate(pos)])

