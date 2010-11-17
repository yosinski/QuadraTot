#! /usr/bin/env python

#import math, pdb, sys
#from numpy import *
#from numpy.linalg import *
#import random
#from copy import copy

from numpy import random, ones, sin
from Strategy import Strategy




def dummyObjective(X):
    '''A Dummy objective that can be used to test learning strategies.
    Intended to be used for vector X where each X is in or close to
    [-1, 1].
    '''

    # Promote to float64 datatype
    X = X * ones(len(X))

    ret = 0.0
    ret += sum(X)
    ret += sum(sin(X/20))

    return ret



def syntheticData(points = 10, dim = 3, fn = dummyObjective):
    '''Generate the requested number of data points from a function.

    Returns of the form:
      [
      (<label>, [(<feature>, <value>), ...]),
      (<label>, [(<feature>, <value>), ...]),
      ...
      ]
    '''

    ret = []
    
    for ii in range(points):
        X = random.randn(dim)
        y = fn(X)
        ret.append( (y, [(ii+1, X[ii]) for ii in range(len(X))]) )

    return ret



class SVMLearningStrategy(Strategy):
    '''
    A strategy that uses the Support Vector Machine regression to
    guess which parameter vector would be good to try next.  Requires
    the installation of "pysvmlight", an interface to SVM Light by
    Thorsten Joachims (http://svmlight.joachims.org/).  pysvmlight is
    available here:

    http://bitbucket.org/wcauchois/pysvmlight
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



def main():
    # copied:
    import svmlight
    import pdb
    
    training_data = syntheticData(30, 1)
    test_data     = syntheticData(30, 1)
    #training_data = __import__('data').train0
    #test_data = __import__('data').test0

    print 'HERE 0'
    print 'training_data is', training_data
    print 'test_data is', test_data

    # train a model based on the data
    #pdb.set_trace()
    print 'HERE 1'
    model = svmlight.learn(training_data, type='regression', kernelType=2, verbosity=3)
    print 'HERE 2'

    # model data can be stored in the same format SVM-Light uses, for interoperability
    # with the binaries.
    svmlight.write_model(model, 'my_model.dat')
    print 'HERE 3'

    # classify the test data. this function returns a list of numbers, which represent
    # the classifications.
    #predictions = svmlight.classify(model, test_data)
    pdb.set_trace()
    predictions = svmlight.classify(model, training_data)
    print 'HERE 4'
    
    for p,example in zip(predictions, test_data):
        print 'pred %.8f, actual %.8f' % (p, example[0])



if __name__ == '__main__':
    main()

