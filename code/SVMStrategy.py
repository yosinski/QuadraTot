#! /usr/bin/env python

#import math, pdb, sys
#from numpy import *
#from numpy.linalg import *
#import random
#from copy import copy


from numpy import array, random, ones, zeros, sin, vstack, hstack, argmax, diag, linalg, dot, exp
from sg import sg           # Import shogun
import pdb

from Strategy import Strategy, OneStepStrategy
from util import *
from SineModel import SineModel5



#    '''
#    A strategy that uses the Support Vector Machine regression to
#    guess which parameter vector would be good to try next.  Requires
#    the installation of "pysvmlight", an interface to SVM Light by
#    Thorsten Joachims (http://svmlight.joachims.org/).  pysvmlight is
#    available here:
#
#    http://bitbucket.org/wcauchois/pysvmlight
#    '''


class SVMLearningStrategy(OneStepStrategy):
    '''
    A strategy that uses the Support Vector Machine regression to
    guess which parameter vector would be good to try next.  Requires
    the installation of shogun-python, a python machine learning
    library offering, among other things, access to libsvr.

    http://www.shogun-toolbox.org/

    http://www.csie.ntu.edu.tw/~cjlin/libsvm/    
    '''

    def __init__(self, *args, **kwargs):
        #if not 'ranges' in kwargs:
        #    raise Exception('SVMLearningStrategy must be called with "ranges" keyword argument.')
        #self.ranges = kwargs.pop('ranges')

        # call this only after popping 'ranges' arg
        super(SVMLearningStrategy, self).__init__(*args, **kwargs)

        N_init_neighborhood = 7
        self.exploreScale = .05
        #self.X = []
        #self.y = []

        # self.current is defined in Strategy constructor

        # 1. Populate toTry with some points
        self.toTry = array(self.current)
        for ii in range(N_init_neighborhood):
            #row = randUniformPoint(self.ranges)
            row = randGaussianPoint(self.current, self.ranges, .1)
            self.toTry = vstack((self.toTry, row))
        
        self.X = None
        self.y = None

    def getNext(self):
        '''Learn model on X and y...'''

        if self.toTry.shape[0] == 0:
            # We're out of things to try.  Make more.
            
            # 1. Learn
            self.train()

            # 2. Try some nearby values
            for ii in xrange(200):
                row = array(randGaussianPoint(self.bestState, self.ranges, self.exploreScale))
                if ii == 0:
                    nearbyPoints = row
                else:
                    nearbyPoints = vstack((nearbyPoints, row))
            predictions = self.predict(nearbyPoints)
            #print 'nearbyPoints', nearbyPoints
            #print 'predicitons', predictions
            
            
            # 3. Pick best one
            iiMax = argmax(predictions)
            self.toTry = array([nearbyPoints[iiMax, :]])

            # 4. (optional) Add a little noise
            self.toTry += randGaussianPoint(zeros(self.toTry.shape[1]),
                                            self.ranges,
                                            .05)

            # UBER HACK!!!!!!!!!!!!!!!!!!
            #self.toTry = array([randUniformPoint(self.ranges)])

            # Prints the most promising vector found and its predicted value
            print '     most promising', prettyVec(self.toTry[0,:]), 'pred: %.2f' % predictions[iiMax]
            
        self.current = self.toTry[0,:]
        return self.current


    def updateResults(self, dist):
        '''This must be called for the last point that was handed out!

        Once called, we remove the first point from self.toTry and add
        it to self.X and add the distance to self.y
        '''

        # MAKE SURE TO CALL super().updateResults!
        super(SVMLearningStrategy, self).updateResults(dist)

        dist = float(dist)
        justTried = self.toTry[0,:]
        self.toTry = self.toTry[1:,:]
        if self.X == None:
            self.X = justTried
            self.y = array(dist)
        else:
            self.X = vstack((self.X, justTried))
            self.y = hstack((self.y, array(dist)))


    def train(self):
        '''Learn a model from self.X and self.y'''

        # Constants pulled from <shogun>/examples/documented/python/regression_libsvr.py
        size_cache=10
        width=2.1
        C=1.2
        epsilon=1e-5
        tube_epsilon=1e-2

        # map each dimension of self.X to [0,1]
        unif = phys2unif(self.X, self.ranges)
        
        train_X = unif.T
        train_y = self.y
        
        sg('set_features', 'TRAIN', train_X)
        sg('set_kernel', 'GAUSSIAN', 'REAL', size_cache, width)

        sg('set_labels', 'TRAIN', train_y)
        sg('new_regression', 'LIBSVR')
        sg('svr_tube_epsilon', tube_epsilon)
        sg('c', C)
        sg('train_regression')


    def predict(self, testPoints):
        '''Predicts performance using previously learned model.
        self.train() must be called before this!'''

        sg('set_features', 'TEST', phys2unif(testPoints,self.ranges).T)
        predictions = sg('classify')

        return predictions


    def plot(self):
        from matplotlib.pyplot import plot, show
        plot(self.y)
        show()



#
# [JBY] The following is just code for testing the SVM/SVR learning
# capabilities.
#

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



def dummyObjectiveGauss(X, center, ranges):
    '''A Dummy objective that can be used to test learning strategies.

    fitness is 100 * GaussianPdf(mean, cov)
    '''

    covar = diag([((x[1]-x[0])*.2) ** 2 for x in ranges])
    
    cinv = linalg.inv(covar)
    return 100. * exp(-dot(dot((X-center), cinv), (X-center)))



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



def syntheticData2(points = 10, dim = 3, fn = dummyObjective):
    '''Generate the requested number of data points from a function.

    Returns of the form:
      X, y   both numpy arrays
    '''

    ret = []

    X = []
    y = []
    for ii in range(points):
        X.append(random.randn(dim))
        y.append(fn(X[-1]))

    return array(X), array(y)



def main_svmlight():
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



def main_libsvr():
    import pdb
    train_X, train_y = syntheticData2(30, 1)
    test_X,  test_y  = syntheticData2(20, 1)

    train_X = train_X.T
    test_X  = test_X.T

    print 'Trying LibSVR'

    size_cache=10
    width=2.1
    C=1.2
    epsilon=1e-5
    tube_epsilon=1e-2

    from sg import sg
    sg('set_features', 'TRAIN', train_X)
    sg('set_kernel', 'GAUSSIAN', 'REAL', size_cache, width)

    sg('set_labels', 'TRAIN', train_y)
    sg('new_regression', 'LIBSVR')
    sg('svr_tube_epsilon', tube_epsilon)
    sg('c', C)
    sg('train_regression')

    sg('set_features', 'TEST', test_X)
    predictions = sg('classify')

    
    for pred,act in zip(predictions, test_y):
        print 'pred %.8f, actual %.8f' % (pred, act)



def main():
    initialPoint = randUniformPoint(SineModel5.typicalRanges)
    strategy = SVMLearningStrategy(initialPoint, ranges = SineModel5.typicalRanges)

    random.seed(3)

    center = array([100, 2, 0, 0, 0])
    obj = lambda x: dummyObjectiveGauss(x, center, SineModel5.typicalRanges)
    
    for ii in range(50):
        print
        print
        current = strategy.getNext()
        print '       trying', prettyVec(current),
        simDist = obj(current)
        print simDist
        strategy.updateResults(simDist)

    strategy.plot()



if __name__ == '__main__':
    main()

