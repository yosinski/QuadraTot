#! /usr/bin/env python

import os, dynamixel, time, random
import datetime
import pdb

from Motion import positionIt
from RobotParams import MIN_INNER, MAX_INNER, MIN_OUTER, MAX_OUTER, MIN_CENTER, MAX_CENTER


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


def main():
    net, actuators = initialize()

    for actuator in actuators:
        actuator.moving_speed = 90
        actuator.synchronized = True
        actuator.torque_enable = True
        actuator.torque_limit = 1000
        actuator.max_torque = 1000

    print 'Starting in 1 sec... ',
    time.sleep(1)
    print 'go.'

    time0 = datetime.datetime.now()
    while True:
        timeDiff = datetime.datetime.now() - time0
        seconds  = timeDiff.seconds + timeDiff.microseconds/1e6

        goal = positionIt(seconds)

        print 'At %3.3f, commanding:' % seconds,

        for ii,actuator in enumerate(actuators):
            gg = goal[ii]
            gg = max(min(gg, servoMax), servoMin)
            actuator.goal_position = gg
            print round(gg, 3),
        net.synchronize()
        print

        #for actuator in actuators[:8]:
        #    actuator.read_all()
        #    time.sleep(0.01)
        #for actuator in actuators[:8]:
        #    print actuator.cache[dynamixel.defs.REGISTER['Id']], actuator.cache[dynamixel.defs.REGISTER['CurrentPosition']]
        time.sleep(.025)

    

        
        
if __name__ == '__main__':
    main()
