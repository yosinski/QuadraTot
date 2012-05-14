#! /usr/bin/env python

#Notes: I'm going to want to make a new RunManager for Rex



import math
import pdb
from math import *
from datetime import *
from time import sleep
from types import FunctionType
from copy import copy
from numpy import array

from Motion import lInterp, scaleTime

from ax12 import *
from driver import Driver

from RobotQuadratot import *
from ConstantsRex import *
from MotionHandler import SmoothMotionFunction



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
            self.port = Driver(portName, 38400, True)
#For some reason, this code gets caught trying to load COM3 instead of COM6.
#My PC usually links to COM6. Just let the user choose the port for now.
#            for i in range(12):
#                portName = "COM" + str(i)
#                try:
#                    self.port = Driver(portName, 38400, True)
#                    break
#                except:
#                    if self.loud: print portName + " not found"
        
        if self.port is None:
            raise Exception("Failed  to open any Serial/COM port")

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
    
    def commandPosition(self, position, crop = True, cropWarning = False, allAtOnce = True):
        '''Set Rex to the given postion as quickly as possible.

        commandPosition will command the robot to move its servos to
        the given position vector.  This vector is cropped to
        the physical limits of the robot and converted to an integer.

        Positional arguments:
        position -- A length 8 vector of desired positions.

        Keyword arguments:
        cropWarning -- Whether or not to print a warning if the
                       positions are cropped.  Default: False.
        allAtOnce -- Whether or not to move the servos using smooth interpolated
                     movements. If false, one servo is adjusted at a time.
        '''
                
        if len(position) != self.nServos:
            raise Exception('Expected postion vector of length %d, got %s instead'
                            % (self.nServos, repr(position)))
        
        goalPosition = None
        if crop:
            goalPosition = self.cropPosition([int(xx) for xx in position], cropWarning)
        else:
            goalPosition = [int(xx) for xx in position]

        if self.loud:
            posstr = ', '.join(['%4d' % xx for xx in goalPosition])
            print '%.2fs -> %s' % (self.time, posstr)
        
        '''if allAtOnce:
            #print "started"
            
            self.tic()
            self.port.execute(253, 7, [18]) #This one isn't too fast either
            self.toc()

            
            #print "1"
            #FIXME
            # download the pose...this step is slow!!!
            self.tic()
            self.port.execute(253, 8, [0] + self.__extract(position))
            self.toc()

            self.tic()
            self.port.execute(253, 9, [0, 244,1,255,0,0])
            self.toc()
            #print "2"
            self.tic()
            self.port.execute(253, 9, [0, 40,0,255,0,0])
            self.toc()
            #print "3"
            self.tic()
            self.port.execute(253, 10, list())
            self.toc()
            #print "made move"
            '''
        if allAtOnce:
            params = [0] * 16
            for i in range(self.nServos):
                params[i*2] = goalPosition[i] >> 8
                params[i*2+1] = goalPosition[i] & 0xff
            self.port.execute(253,132, params)
                
        else:
            for servo in range(self.nServos):
                pos = position[servo]
                self.port.setReg(servo+1, P_GOAL_POSITION_L, [pos%256, pos>>8])
        
        self.commandsSent += 1
        return goalPosition
    
    def __extract(self, li):
        """ extract x%256,x>>8 for every x in li """
        out = list()
        for i in li:
            ii = int(i)
            out = out + [ii%256,ii>>8]
        return out
    
    '''Rewrite for compatibility with old code'''
    def __commandPositionWithTime(self, start, end, seconds, logFile=None, extraLogInfoFn=None):
        '''Moves between start and end over seconds seconds.  start
        and end are position vectors.'''
        
        seconds *= 1000
        dt = int(seconds)
        
        poseDL = dict()     # key = pose name, val = index, download them after we build a transition list
        tranDL = list()     # list of bytes to download
        
        poseDL[0] = 0 #start
        poseDL[1] = 1 #end

        # create transition values to download
        tranDL.append(poseDL[0])                # ix of pose
        tranDL.append(244)                   # time is an int (16-bytes)
        tranDL.append(1)
        
        tranDL.append(poseDL[1])
        tranDL.append(dt % 256)
        tranDL.append(dt >> 8)
        
        tranDL.append(255)      # notice to stop
        tranDL.append(0)        # time is irrelevant on stop    
        tranDL.append(0)
        
        self.port.execute(253, 7, [18])
        # send poses
        self.port.execute(253, 8, [0] + self.__extract(start))
        self.port.execute(253, 8, [1] + self.__extract(end))#should [1] be [0]?
        print "Sending sequence: " + str(tranDL)
        # send sequence and play            
        self.port.execute(253, 9, tranDL)
        self.port.execute(253, 10, list())
        
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
            
        
    
    def commandFunction(self, smoothFnct, loop=False):
        '''Executes motions determined by the given motion function
        smoothFnct --- a SmoothMotionFunction instance
        loop --- if true, the function will execute in a cycle'''
        
        fnct = smoothFnct.motionFnct
        times = smoothFnct.times
        
        dt = int(times[1] - times[0]) * 1000 # delta-T
        
        poseDL = dict()     # key = pose name, val = index, download them after we build a transition list
        tranDL = list()     # list of bytes to download
        
        #Set up the first pose
        poseDL[0] = 0
        tranDL.append(poseDL[0])
        tranDL.append(244)
        tranDL.append(1)
        for i in range(1,len(times)):#TODO: start at 1?
            poseDL[i] = len(poseDL.keys())          # get ix for pose
            # create transition values to download
            tranDL.append(poseDL[i])                # ix of pose
            tranDL.append(dt%256)                   # time is an int (16-bytes)
            tranDL.append(dt>>8)
        tranDL.append(255)      # notice to stop
        tranDL.append(0)        # time is irrelevant on stop    
        tranDL.append(0)
        # set pose size -- IMPORTANT!
        self.port.execute(253, 7, [18])
        # send poses
        print "Sending poses: " + str(len(poseDL.keys()))
        for p in poseDL.keys():
            self.port.execute(253, 8, [poseDL[p]] + self.__extract(fnct[p]))
        # send sequence and play
        print "Sending sequences"
        self.port.execute(253, 9, tranDL)
        # run or loop?
        print "Running or looping?"
        if loop: #TODO: Figure out if the 'if' or 'else' is the loop one.
            self.port.execute(253,11,list())
        else:
            self.port.execute(253, 10, list())
    
    '''Rewrite if desired'''
    def cropPosition(self, position, cropWarning = False):
        '''Crops the given positions to their appropriate min/max values.
        
        Requires a vector of length 8 to be sure the IDs are in the
        assumed order.'''

        if len(position) != self.nServos:
            raise Exception('cropPosition expects a vector of length %d' % self.nServos)

        ret = copy(position)
        for ii in [0, 2, 4, 6]:
            ret[ii]   = max(MIN_INNER, min(MAX_INNER, ret[ii]))
            ret[ii+1] = max(MIN_OUTER, min(MAX_OUTER, ret[ii+1]))

        if cropWarning and ret != position:
            print 'Warning: cropped %s to %s' % (repr(position), repr(ret))
            
        return ret
    
    def readCurrentPosition(self):
        '''Reads in the position vector of the servos. Will fail if the servos
        are receiving a command from interpMove()'''
        ret = []
        for servo in range(self.nServos):
            pos = self.port.getReg(servo+1,P_PRESENT_POSITION_L, 2)
            try:
                ret.append(str(pos[0] + (pos[1]<<8)))
            except TypeError:
                print "Failed to read the servos"
                return None
        return ret
    
    '''Rewrite if desired???'''
    def pingAll(self):
        failures = []
        for ii in self.actuatorIds:
            result = self.net.ping(ii)
            if result is False:
                failures.append(ii)
        return failures
    
    def relax(self):
        '''Relaxes servos. Use when we are done with a motion sequence.'''
        for servo in range(self.nServos):
            self.port.setReg(servo+1,P_TORQUE_ENABLE, [0,])   

if __name__ == "__main__":
    robot = RobotRex(8, "COM6", cmdRate = 14)
    pos0 = [0] * 8
    pos1 = [270] * 8
    pos2 = [0,0,0,0,270,270,270,270]
    
    pi = math.pi
    
    dur = 100.0
    start = lambda t: (abs(200.0*sin(pi*t)),0.0,
                       abs(270.0/dur*t*sin(pi*t)), 125.0,
                       t*270.0/dur, (1-t/dur)*270.0,
                       270.0*(t/dur)**3,25.0)
    end = lambda t: ([135.0] * 8)
    
    f1 = lambda t: (abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
                    abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
                    abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
                    abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)))
    sleep(2)

#    print "sending first"
#    robot.interpMove2(pos0,pos0,2)
#    print "sent first"
#    sleep(3)
#    print "sending second"
#    robot.commandPosition(pos1)
#    print "sent second"
#    print "starting function"
#    robot.interpMove(start,end,4)
#    print "Commands sent: " + str(robot.commandsSent)
    print robot.sleep
    print "starting position"
    robot.interpMove2(f1,f1,dur)
    print "Commands sent: " + str(robot.commandsSent)

    pdb.set_trace()

    #robot.commandFunction(myFunction)
#    sleep(1)
#    print "relaxing"
#    robot.relax()
#    robot.commandPosition(pos0)
#    sleep(2)
#    print robot.readCurrentPosition()
#    sleep(.5)
#    print "About to interpMove"
#    robot.interpMove(pos0, pos1, 10)
#    sleep(3)
#    print robot.readCurrentPosition()
#    robot.relax()