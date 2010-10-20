'''
date: 20 October 2010

'''
"""
2) neighbor selection (uniform change of one parameter, gaussian
change of one parameter, gaussian change of multiple parameters, ...)

"""

import math, pdb, sys
import random
from copy import copy

class Neighbor:
    @staticmethod
    def uniform(ranges, parameters):
        """
        Uniform change of one parameter: Given a list of parameters, picks a
        random parameter to change, randomly changes it, and returns a new 
        list.
    
        """
        ret = copy(parameters)

        index = random.randint(0, len(parameters) - 1)

        #print ranges
        if isinstance(ranges[index][0], bool):
            ret[index] = (random.uniform(0,1) > .5)
        else:
            ret[index] = random.uniform(ranges[index][0], ranges[index][1])

        #print '  ** Neighbor new', ret
        return ret

    @staticmethod
    def uniform_slight(ranges, parameters):
        """
        Given a list of parameters, picks a random parameter to change, and
        decreases or increases it slightly.
    
        """
        ret = copy(parameters)
        print '  ** Neighbor old', ret
        index = random.randint(0, len(parameters) - 1)
    
        print ranges
        if isinstance(ranges[index][0], bool):
            ret[index] = (random.uniform(0,1) > .5)
        else:
            if random.randint(0, 1) == 0:  # decrease slightly
                ret[index] = ret[index] - (.1 * (ranges[index][1] - ranges[index][0]))
            else:  # increase slightly
                ret[index] = ret[index] - (.1 * (ranges[index][1] - ranges[index][0]))
    
        print '  ** Neighbor new', ret
        return ret
    
    @staticmethod
    def gaussian(ranges, parameters):
        """
        Gaussian change of one parameter:
        Given a list of parameters, picks a random parameter to change, 
        randomly changes it based on a Gaussian distribution, and returns
        a new list.
    
        """
        ret = copy(parameters)
        index = random.randint(0, len(parameters) - 1)
    
        if isinstance(ranges[index][0], bool):
            ret[index] = (random.uniform(0,1) > .5)
        else:
            while True:
                changeTo = random.gauss(ret[index], .10 * (ranges[index][1] - 
                                                           ranges[index][0]))
                # Check that randomly generated number is in range
                if ranges[index][0] <= changeTo <= ranges[index][1]:
                    ret[index] = changeTo
                    break
    
        return ret