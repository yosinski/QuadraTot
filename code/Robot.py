import os, dynamixel, time, datetime
from RobotParams import *
from Motion import lInterp

def initialize():
    '''Creates a network and scans it for servos.

    Returns (network, actuatorList)
    '''
    # The number of Dynamixels on our bus.
    nServos = 11

    # Set your serial port accordingly.
    if os.name == "posix":
        portName = "/dev/ttyUSB0"
    else:
        portName = "COM11"

    # Default baud rate of the USB2Dynamixel device.
    baudRate = 1000000

    serial = dynamixel.SerialStream( port=portName, baudrate=baudRate, timeout=1)
    net = dynamixel.DynamixelNetwork( serial )
    net.scan( 0, nServos )

    actuators = list()

    print "Scanning for Dynamixels...",
    for dyn in net.get_dynamixels():
        print dyn.id,
        actuators.append(net[dyn.id])
    print "...Done"

    return net, actuators


def runRobotWith(paramFunction, runSeconds = 10):
    net, actuators = initialize()

    for actuator in actuators:
        actuator.moving_speed = 90
        actuator.synchronized = True
        actuator.torque_enable = True
        actuator.torque_limit = 1000
        actuator.max_torque = 1000

    print 'Starting in 0 sec... ',
    #time.sleep(1)
    print 'go.'

    time0 = datetime.datetime.now()
    startingPos = None
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

        for ii,actuator in enumerate(actuators):
            gg = int(round(goal[ii],0))
            #gg = max(min(gg, servoMax), servoMin)
            actuator.goal_position = gg
            #print gg,
        net.synchronize()
        #print

        #for actuator in actuators[:8]:
        #    actuator.read_all()
        #    time.sleep(0.01)
        #for actuator in actuators[:8]:
        #    print actuator.cache[dynamixel.defs.REGISTER['Id']], actuator.cache[dynamixel.defs.REGISTER['CurrentPosition']]
        time.sleep(.025)



def cropPositions(pos):
    '''Crops the given positions to their appropriate min/max values.
    Requires a vector of length 9 to be sure the IDs are in the
    assumed order.'''

    if len(pos) != 9:
        raise Exception('cropPositions expects a vector of length 9')

    for ii in [0, 2, 4, 6]:
        pos[ii]   = max(MIN_INNER, min(MAX_INNER, pos[ii]))
        pos[ii+1] = max(MIN_OUTER, min(MAX_OUTER, pos[ii+1]))
    pos[8] = max(MIN_CENTER, min(MAX_CENTER, pos[8]))



def currentPositions(actuators):
    ret = []
    for ac in actuators:
        ac.read_all()
        ret.append(ac.cache[dynamixel.defs.REGISTER['CurrentPosition']])
    return ret



def printStatus(actuators):
    pos = currentPositions(actuators)
    print 'Positions:', ' '.join(['%d:%d' % (ii,pp) for ii,pp in enumerate(pos)])


