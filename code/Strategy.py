#! /usr/bin/env python

'''
date: 20 October 2010

'''
"""
Neighbor selection (uniform change of one parameter, gaussian
change of one parameter, gaussian change of multiple parameters, ...)

"""

import math, pdb, sys
from numpy import *
from numpy.linalg import *
import random
from copy import copy
from util import prettyVec

class Strategy(object):
    '''Base class for strategies.'''

    def __init__(self, initialPoint):
        self.current = initialPoint
        self.iterations = 0
        self.bestIter   = None
        
    def getNext(self, ranges):
        raise Exception('Need to implement this')

    def updateResults(self, dist, ranges):
        '''This must be called for the last point that was handed out!'''
        raise Exception('Need to implement this')


class OneStepStrategy(Strategy):
    """
    Base class for any methods that produce a single neighbor at a time.
    """

    def __init__(self, *args, **kwargs):
        super(OneStepStrategy, self).__init__(*args, **kwargs)
        self.bestDist  = None
        self.bestState = self.current
        
    def updateResults(self, dist, ranges):
        self.iterations += 1
        if self.bestDist is None or dist > self.bestDist:
            self.bestDist = dist
            self.bestState = self.current
            self.bestIter  = self.iterations

        print '    best (iter %3d)' % self.bestIter, prettyVec(self.bestState), '%.2f' % self.bestDist  # Prints best state and distance so far


class RandomStrategy(OneStepStrategy):
    """
    Random change of all parameters: Given a list of parameters, randomly
    changes all of them, and returns a new list.
    
    """

    def getNext(self, ranges):
        ret = copy(self.bestState)

        if self.bestDist is not None:
            for index in range(0, len(ret)):
                #print ranges
                if isinstance(ranges[index][0], bool):
                    ret[index] = (random.uniform(0,1) > .5)
                else:
                    ret[index] = random.uniform(ranges[index][0], \
				                ranges[index][1])

        #print '  ** Neighbor new', ret
        return ret

class UniformStrategy(OneStepStrategy):
    """
    Uniform change of one parameter: Given a list of parameters, picks
    a random parameter to change, randomly changes it, and returns a
    new list.
    
    """

    def getNext(self, ranges):
        ret = copy(self.bestState)

        if self.bestDist is not None:
            index = random.randint(0, len(ranges) - 1)

            #print ranges
            if isinstance(ranges[index][0], bool):
                ret[index] = (random.uniform(0,1) > .5)
            else:
                ret[index] = random.uniform(ranges[index][0], ranges[index][1])

        #print '  ** Neighbor new', ret
        return ret

    

class UniformSlightStrategy(OneStepStrategy):
    """
    Given a list of parameters, picks a random parameter to change, and
    decreases or increases it slightly.
    
    """

    def getNext(self, ranges):
        ret = copy(self.bestState)
        print '  ** Neighbor old', ret
        index = random.randint(0, len(parameters) - 1)
        print ranges
        if isinstance(ranges[index][0], bool):
            ret[index] = (random.uniform(0,1) > .5)
        else:
            if random.randint(0, 1) == 0:  # decrease slightly
                ret[index] = ret[index] - (.1 * (ranges[index][1] - ranges[index][0]))
            else:  # increase slightly
                ret[index] = ret[index] + (.1 * (ranges[index][1] - ranges[index][0]))
    
        print '  ** Neighbor new', ret
        return ret



class GaussianStrategy(OneStepStrategy):
    """
    Gaussian change of all parameter:
    Given a list of parameters, randomly changes all parameters based on a
    Gaussian distribution, and returns a new list.
    
    """

    def getNext(self, ranges):
        ret = copy(self.bestState)
        index = random.randint(0, (len(ranges) - 1))
    
        for index in range(len(ranges)):
            if isinstance(ranges[index][0], bool):
                ret[index] = (random.uniform(0,1) > .5)
            else:
                while True:
                    changeTo = random.gauss(ret[index], .05 * (ranges[index][1] - 
                                                           ranges[index][0]))
                    # Check that randomly generated number is in range
                    if ranges[index][0] <= changeTo <= ranges[index][1]:
                        ret[index] = changeTo
                        break
    
        return ret



class GradientSampleStrategy(Strategy):
    """
    N-dimensional policy gradient algorithm. During each iteration of the main
    loop we sample t policies near currentState to estimate the gradient
    around currentState, then move currentState by an amount of eta in the
    most favorable direction. Adapted from Nate Kohl and Peter Stone,
    UT Ausin/ICRA 2004.
    
    """

    def __init__(self, *args, **kwargs):
        super(GradientSampleStrategy, self).__init__(*args, **kwargs)
        self.bestDist  = None
        self.bestState = self.current

        self.epsilon = .05
        self.numNeighbors = 8

        self.triedSoFar = []
        self.stillToTry = []

    def getNext(self, ranges):
        if len(self.stillToTry) == 0:
            self.populateStillToTry(ranges)

        return self.stillToTry[0]

    def populateStillToTry(self, ranges):
        self.stillToTry.append(self.current)

        # Evaluate t=8 policies per iteration
        print 'Base  point is', self.current
        for i in range(self.numNeighbors):
            point = self.getEpsilonNeighbor(ranges, self.current, self.epsilon)
            print 'Nearby point is', point
            self.stillToTry.append(point)
        

    def updateResults(self, dist, ranges):
        '''This must be called for the last point that was handed out!'''

        self.triedSoFar.append(self.stillToTry.pop(0))
        self.triedSoFar[-1].append(dist)
        print '        Got update, policy is now', self.triedSoFar[-1]

        # If this was the last one, compute a new current location
        if len(self.stillToTry) == 0:
            self.current = self.computeNextMove(self.current, ranges, self.triedSoFar)
            self.triedSoFar = []
            self.stillToTry = []


    def getEpsilonNeighbor(self, ranges, parameters, epsilon):
        """
        Given a list of parameters, returns a randomly generated policy nearby
        such that each parameter is changed randomly by +epsilon * range, 0, 
        or -epsilon * range.
    
        """
        ret = copy(parameters)
        #print 'ret was', ret
        for index in range(len(parameters)):
            param = random.choice((0, 1, 2))
            if param == 0:  # decrease by epsilon*range
                change = ret[index] - (epsilon * (ranges[index][1] - ranges[index][0]))
                if change < ranges[index][0]:  # Check that we are within range.
                    ret[index] = ranges[index][0]
                else:
                    ret[index] = change
            if param == 1:  # increase by epsilon*range
                change = ret[index] + (epsilon * (ranges[index][1] - ranges[index][0]))
                if change > ranges[index][1]:
                    ret[index] = ranges[index][1]
                else:
                    ret[index] = change
        #print 'returning', ret
        #print
        return ret

    def computeNextMove(self, center, ranges, samples):
        '''Returns the center of the next distribution.'''

        # Average the scores for all random policies
        adjustment = []  # Adjustment vector
        for n in range(len(ranges)):
             # Keep track of number of policies with pos/neg/0 perturbation
             # in dimension n
            num_epos = num_eneg = num_zero = 0
            avg_epos = avg_eneg = avg_zero = 0
            for neighbor in samples:
                if neighbor[n] > center[n]:  # positive perturbation
                    avg_epos = avg_epos + neighbor[len(neighbor) - 1]
                    num_epos = num_epos + 1
                if neighbor[n] < center[n]:  # negative perturbation
                    avg_eneg = avg_eneg + neighbor[len(neighbor) - 1]
                    num_eneg = num_eneg + 1
                if neighbor[n] == center[n]:  # zero perturbation
                    avg_zero = avg_zero + neighbor[len(neighbor) - 1]
                    num_zero = num_zero + 1

            # Finish calculating averages.        
            try:
                avg_epos = avg_epos / num_epos
            except ZeroDivisionError:
                avg_epos = 0

            try: 
                avg_eneg = avg_eneg / num_eneg
            except ZeroDivisionError:
                avg_eneg = 0

            try:
                avg_zero = avg_zero / num_zero
            except ZeroDivisionError:
                avg_zero = 0

            if avg_zero > avg_epos and avg_zero > avg_eneg:
                adjustment.append(0)
            else:
                adjustment.append(avg_epos - avg_eneg)

		# Calculate adjustment vector for each dimension, multiplying with a
		# scalar step-size eta, so that our adjustment will remain a fixed
		# size each iteration
		eta = .1
		total = 0
		for adj in adjustment:
		    total += adj ** 2
		magnitude = math.sqrt(total)
		
		for index in range(len(adjustment)):
			adjustment[index] = (adjustment[index] / magnitude) * eta
			adjustment[index] = adjustment[index] * (ranges[index][1] - ranges[index][0])

        nextState = [center, adjustment]
        return [sum(value) for value in zip(*nextState)]



class LearningStrategy(Strategy):
    '''
    A strategy that uses supervised learning to guess which parameter vector would be good to try next.
    '''

    def __init__(self, *args, **kwargs):
        super(LearningStrategy, self).__init__(*args, **kwargs)
        self.X = []
        self.y = []

    def getNext(self, ranges):
        '''Learn model on X and y...'''

        # 1. Learn
        # 2. Try some nearby values
        # 3. Pick best one


    def updateResults(self, dist, ranges):
        '''This must be called for the last point that was handed out!'''

        # about the same...
        self.triedSoFar.append(self.stillToTry.pop(0))
        self.triedSoFar[-1].append(dist)
        print '        Got update, policy is now', self.triedSoFar[-1]

class LinearRegressionStrategy(LearningStrategy):
    '''
    A strategy that uses supervised learning (linear regression) to guess which
    parameter vector would be good to try next.
    '''

    def __init__(self, *args, **kwargs):
        super(LearningStrategy, self).__init__(*args, **kwargs)
        self.X = []
        self.y = []

    def getNext(self, ranges):
        '''Learn model on X and y...'''

        # 1. Learn
        # 2. Try some nearby values
        # 3. Pick best one


    def updateResults(self, dist, ranges):
        '''This must be called for the last point that was handed out!'''

        # about the same...
        self.triedSoFar.append(self.stillToTry.pop(0))
        self.triedSoFar[-1].append(dist)
        print '        Got update, policy is now', self.triedSoFar[-1]

    def predict_distance_walked(self, weights, inputs):
        '''
        Given a weight vector and an input vector, predicts the distance
        walked by the robot.        
        '''
        return sum([weights[i]*inputs[i] for i in range(len(weights))])

    def calculate_weights(self, training_params, distances_walked):
        '''
        Given matching vectors of training parameter vectors and the distances
        walked by each training param, of length, calculates an initial 
        guess for the weights using least-squares
        '''
        x = linalg.lstsq(training_params, distances_walked)
        return x

if __name__ == "__main__":
    import doctest
    doctest.testmod()
            

    # # [JBY] This can be put in a unit test instead
    # # Testing Neighbor.gradient function...
    # ranges = [(0, 400), (.5, 8), (-2, 2), (-1, 1), (-1, 1)]
    # 
    # parameters = []  # List of the chosen values for the parameters
    # for rang in ranges:
    #     # Chooses random values for each parameter (initial state)
    #     if isinstance(rang[0], bool):  # If range is (true, false),
    #         # choose true or false
    #         parameters.append(random.uniform(0,1) > .5)
    #     else:
    #         parameters.append(random.uniform(rang[0], rang[1]))
    # print parameters
    # print Neighbor.gradient(ranges, parameters, .05)
    # print Neighbor.gaussian(ranges, parameters)

    
