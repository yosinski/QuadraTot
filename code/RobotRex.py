#! /usr/bin/env python

#Notes: I'm going to want to make a new RunManager for Rex



import math
from math import *
from datetime import *
from time import sleep
from types import FunctionType
from numpy import array, interp

from ax12 import *
from driver import Driver

from RobotQuadratot import *
from ConstantsRex import *


def lInterp(time, theDomain, val1, val2):
    ret = []
    for ii in range(len(val1)):
        ret.append(interp([time], theDomain, [val1[ii], val2[ii]])[0])
    return ret

class RobotRex(RobotQuadratot):
    ''''''

    def __init__(self, nServos, portName="", cmdRate=40):
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
        
        RobotQuadratot.__init__(self, commandRate=cmdRate, skipInit=True)
        self.commandsSent = 0
        self.nServos = nServos
        
        #Find a valid port.
        if os.name == "posix":
            possibilities = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/cu.usbserial-A800KDV8']
            for pos in possibilities:
                if os.path.exists(pos):
                    portName = pos
            if portName is None:
                raise Exception('Could not find any of %s' % repr(possibilities))
            self.port = Driver(portName, 38400, True)
        else:
            if portName is None:
                portName = 'COM6'
            #self.port = Driver(portName, 38400, True)
            self.port = None
        
#        if self.port is None:
#            raise Exception("Failed  to open any Serial/COM port")

        self.currentPos = None
        self.resetClock()

    '''REWRITE IF DESIRED'''
    def readyPosition(self, persist = False):
        if persist:
            self.resetClock()
            while self.time < 2.0:
                self.commandPosition(POS_READY)
                sleep(.1)
                self.updateClock()
        else:
            self.commandPosition(POS_READY)
            sleep(2)
    
    def __extract(self, li):
        """ extract x%256,x>>8 for every x in li """
        out = list()
        for i in li:
            ii = int(i)
            out = out + [ii%256,ii>>8]
        return out
        
    def interpMove2(self, start, end, seconds):
        '''Performs the same function as interpMove() in RobotQuadratot but uses
        the new interface that I wrote up for Aracna.
            start -- a postion vector/function
            end -- a position vector/function
            seconds -- the duration the two functions should be interpolated over'''
        self.updateClock()
        
        timeStart = self.time
        timeEnd   = self.time + seconds
        
        print timeStart
        print timeEnd

        while self.time < timeEnd:
            #print 'time:', self.time
            self.updateClock()
            posS = start(self.time) if isinstance(start, FunctionType) else start
            posE =   end(self.time) if isinstance(end,   FunctionType) else end
            goal = lInterp(self.time, [timeStart, timeEnd], posS, posE)
            
            #print goal
            
            #write out the command to the robot
            self.commandOverTime(goal, int(self.sleep * 1000))
    
    def commandOverTime(self, pos, dur):
        '''Writes out a packet to the robot to execute the commandOverTime
        function. Stalls after the command is sent to prevent overflowing the
        buffer on the robot.
            pos -- a position vector. Values are in the range [0,270]
            dur -- the duration (in milliseconds) of the transition'''
        dur1 = dur >> 8
        dur2 = dur & 0x00ff
        
        posArr = [0] * (self.nServos * 2)
        for i in range(self.nServos):
            posArr[2 * i] = int(pos[i]) >> 8
            posArr[2*i+1] = int(pos[i]) & 0x00ff
        
        startTime = datetime.now()
        
        #print "sending command" + str(datetime.now())
        newPos = self.port.execute2(COMMAND_OVER_TIME, [dur1, dur2] + posArr)
        
        #Calculate the real position vector and print it out
        if newPos is not None:
            realPos = [0] * 8
            for i in range(self.nServos): realPos[i] = (newPos[i*2] << 8) + (newPos[i*2+1])
            print realPos
        
        endTime = startTime + timedelta(0,self.sleep)
        while datetime.now() < endTime: sleep(self.sleep/20)
    
    def relax(self):
        '''Relaxes servos. Use when we are done with a motion sequence.'''
        for servo in range(self.nServos):
            self.port.setReg(servo+1,P_TORQUE_ENABLE, [0,])   

if __name__ == "__main__":
    robot = RobotRex(8, "COM6", cmdRate = 14)
    pi = math.pi
    
    dur = 100.0
    
    f1 = lambda t: (abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
                    abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
                    abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
                    abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)))
    sleep(2)

    robot.interpMove2(f1,f1,dur)