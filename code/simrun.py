import math, pdb, sys
import random
import os
import string
from datetime import datetime
from copy import copy
from time import sleep
from RobotConstants import MIN_INNER, MAX_INNER, MIN_OUTER, MAX_OUTER, MIN_CENTER, MAX_CENTER, NORM_CENTER

class simrun:
    ''' simulation running '''

    def __init__(self):
        self.filename = "output.txt"
 
    def runSim(self, gaitFunction):
        ff = file('input.txt', "w")
        timeMax = 12.0
        timeDiv = 1.0/12.0
        divs = timeMax/timeDiv
        t = 0.0

        for i in xrange(0,limit): 
            gait = gaitFunction(t)
            t = t+div
            if t == timeMax:
                file.write(str(t) + ' ' + str(gait))
            else:
                file.write(str(t) + ' ' + str(gait) + '\n')
            
            
        os.system('./physXsimulator -i input.txt -o output.txt')
        dist = self.getDist()      
                
    def getDist(self):

	outputRaw= file(self.filename,"r")
	outputData = [line.split() for line in outputRaw]
        outputColLen = len(outputData)-1
        outputRowLen = len(outputData[1])-1
        posBeg = [outputData[1][outputRowLen-2], outputData[1][outputRowLen-1], outputData[1][outputRowLen]]
        posEnd = [outputData[outputColLen][outputRowLen-2], outputData[outputColLen][outputRowLen-1], outputData[outputColLen][outputRowLen]]

        # finds the distance the robot travelled using x and y '
        xdist = float(posEnd[0])-float(posBeg[0])
        ydist = float(posEnd[1])-float(posBeg[1])
#        zdist = float(self.posEnd[2])-float(self.posBeg[2])
        return math.sqrt(math.pow(xdist,2)+math.pow(ydist,2))

    def cropPosition(self, position, cropWarning = False):
        # crops the given positions to their apropriate min/max values.
        #Requires a vector of length 9 to be sure the IDs are in the assumed order.'''
        ret = copy(position)
        for ii in [0, 2, 4, 6]:
            ret[ii] = max(MIN_INNER, min(MAX_INNER, ret[ii]))
            ret[ii+1] = max(MIN_OUTER, min(MAX_OUTER, ret[ii+1]))
        ret[8] = max(MIN_CENTER, min(MAX_CENTER, ret[8]))

        if cropWarning and ret != position:
            print 'Warning: cropped %s to %s' % (repr(position), repr(ret))

        return ret

    
