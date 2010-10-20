import math, pdb, sys
import random
from datetime import datetime
from copy import copy
from Robot import Robot
from SineModel import sineModel

class RunManager:

    @staticmethod
    def initialState(ranges):
        """ 
        Given the ranges of the different parameters, chooses random values for
        each parameter. The ranges of parameters are in a list of tuples.
    
        """
        parameters = []  # List of the chosen values for the parameters
        for rang in ranges:
            # Chooses random values for each parameter (initial state)
            if isinstance(rang[0], bool):  # If range is (true, false),
                           # choose true or false
                parameters.append(random.uniform(0,1) > .5)
            else:
                parameters.append(random.uniform(rang[0], rang[1]))
        return parameters
    
    @staticmethod
    def prettyVec(vec):
        return ('[' +
                ' '.join(['%4f' % xx if isinstance(xx,float) else repr(xx) for xx in vec]) +
                ']')
        
    @staticmethod
    def log_start():
        logFile = open('log.txt', 'a')
        logFile.write('\nOptimize started at %s\n' % datetime.now().ctime())
        logFile.close()
        
    @staticmethod
    def write_log(currentState, currentDistance):
        """Writes to log file that keeps track of tests so far"""
        stats = ' '.join([repr(xx) for xx in currentState])
        logFile = open('log.txt', 'a')
        logFile.write(stats + ", " + str(currentDistance) + "\n")
        logFile.close()