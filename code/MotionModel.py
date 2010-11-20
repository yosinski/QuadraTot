

def randUniformState(ranges):
    '''
    Given the ranges of the different parameters, chooses random values for
    each parameter. The ranges of parameters are in a list of tuples.

    '''

    parameters = []  # List of the chosen values for the parameters
    for rang in ranges:
        # Chooses random values for each parameter (initial state)
        if isinstance(rang[0], bool):  # If range is (true, false),
                       # choose true or false
            parameters.append(random.uniform(0,1) > .5)
        else:
            parameters.append(random.uniform(rang[0], rang[1]))
    return parameters
    
class MotionModel(object):
    '''Base class for all motion models'''
    
    def model(self, *args, **kwargs):
        '''Override this method to make your own motion model.

        This method should take the time and other optional parameters
        '''
        
        raise Exception('Not implemented')
