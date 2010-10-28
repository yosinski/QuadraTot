import math, pdb, sys
import random
from datetime import datetime
from copy import copy
from Robot import Robot
from SineModel import sineModel
from wii.WiiTrackClient import WiiTrackClient

class RunManager:
    '''Manage runs..'''

    def __init__(self):
        self.robot = Robot(commandRate = 40, loud = False)
        self.statesSoFar = set()  # Keeps track of the states tested so far
        
    def initialState(self, ranges):
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
    
    # TODO: Am I calling stuff in here correctly..?
    def run_robot(self, currentState):
        """
        Runs the robot with currentState's parameters and returns the
        distance walked.
        
        """
        motionModel = lambda time: sineModel(time,
                                             parameters = currentState)

        wiiTrack = WiiTrackClient("localhost", 8080)
        beginPos = wiiTrack.getPosition()
        if beginPos is None:
            # Robot walked out of sensor view
            self.manual_reset()
            print 'Retrying last run'
            return self.run_robot(currentState)
        
        self.robot.run(motionModel, runSeconds = 10, resetFirst = False,
                       interpBegin = 1, interpEnd = 1)

        endPos = wiiTrack.getPosition()
        if endPos is None:
            # Robot walked out of sensor view
            self.manual_reset()
            print 'Retrying last run'
            return self.run_robot(currentState)

        distance_walked = self.calculate_distance(beginPos, endPos)
        print '        walked %.2f' % distance_walked
    
        return distance_walked
    
    def prettyVec(self, vec):
        return ('[' +
                ' '.join(['%4f' % xx if isinstance(xx,float) else repr(xx) for xx in vec]) +
                ']')
        
    def log_start(self):
        logFile = open('log.txt', 'a')
        logFile.write('\nOptimize started at %s\n' % datetime.now().ctime())
        logFile.close()
        
    def write_log(self, currentState, currentDistance):
        """Writes to log file that keeps track of tests so far"""
        stats = ' '.join([repr(xx) for xx in currentState])
        logFile = open('log.txt', 'a')
        logFile.write(stats + ", " + str(currentDistance) + "\n")
        logFile.close()

    def calculate_distance(self, begin, end):
        """
        Calculates how far the robot walked given the beginning and ending
        (x, y) coordinates.
        """
        return math.sqrt(pow((end[0] - begin[0]), 2) + pow((end[1] - begin[1]), 2))

    def do_many_runs(self, initialState, neighborFunction, limit = None):
        if limit is None:
            limit = 10000

        bestDistance = -1e100

        currentState = initialState

        self.log_start()

        for ii in xrange(limit):
            print
            print 'Iteration %2d params' % ii, self.prettyVec(currentState)

            # Check if this state is new, and possibly skip it
            if tuple(currentState) in self.statesSoFar:
                print '*** Duplicate iteration!'
                # Skip only if using random hill climbing. In other words,
                # comment this line out if using gradient_search:
#                currentState = neighborFunction(bestState)
                continue

            currentDistance = self.run_robot(currentState)

            self.statesSoFar.add(tuple(currentState))

            print '        walked %.2f' % currentDistance

            if currentDistance >= bestDistance:  # Is this a new best?
                bestState = copy(currentState)  # Save new neighbor to best found
                bestDistance = copy(currentDistance)

            print '        best so far', self.prettyVec(bestState), '%.2f' % bestDistance  # Prints best state and distance so far

            self.write_log(currentState, currentDistance)

            currentState = neighborFunction(bestState)

    def manual_reset(self):
        print 'Robot has walked outisde sensor view.  Please place back in center and push enter to continue.'
        raw_input()
