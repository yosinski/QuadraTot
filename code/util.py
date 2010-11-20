#! /usr/bin/env python

'''Just a few utility functions'''

def prettyVec(vec):
    return ('[' +
            ' '.join(['%4f' % xx if isinstance(xx,float) else repr(xx) for xx in vec]) +
            ']')



def randUniformPoint(ranges):
    '''
    Given the ranges of the different parameters, chooses random values for
    each parameter. The ranges of parameters are in a list of tuples.

    '''

    import random
    parameters = []  # List of the chosen values for the parameters
    for rang in ranges:
        # Chooses random values for each parameter (initial state)
        if isinstance(rang[0], bool):  # If range is (true, false),
                       # choose true or false
            parameters.append(random.uniform(0,1) > .5)
        else:
            parameters.append(random.uniform(rang[0], rang[1]))
    return parameters
    
